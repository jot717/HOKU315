"""
Supabase：lru_cache 單例連線；profiles 向量、user_memories（RAG Lite）與 RPC。

預設（可透過環境變數覆寫）：
  _VECTOR_COL -> vector
  _MATCH_RPC -> get_safe_matches
  _MATCH_RPC_VEC_PARAM -> query_vector
  _MATCH_RPC_THRESHOLD_PARAM -> match_threshold
  user_memories 表與 match_user_memories RPC 見 sql/user_memories.sql
  stories 表見 sql/stories.sql；需使用使用者 JWT + anon key 以通過 RLS
  user_unlocks 見 sql/user_unlocks.sql
"""
from __future__ import annotations

import ast
import os
import re
import time
from functools import lru_cache
from pathlib import Path
from typing import Any, BinaryIO, Optional, Union

from dotenv import load_dotenv
from postgrest.types import ReturnMethod
from supabase import Client, create_client

_ROOT = Path(__file__).resolve().parent
load_dotenv(_ROOT / ".env", encoding="utf-8-sig")
load_dotenv(encoding="utf-8-sig")

_VECTOR_COL = os.getenv("SUPABASE_PROFILES_VECTOR_COLUMN", "vector")
_MATCH_RPC = os.getenv("SUPABASE_VECTOR_MATCH_RPC", "get_safe_matches")
_MATCH_RPC_VEC_PARAM = os.getenv("SUPABASE_MATCH_RPC_VEC_PARAM", "query_vector")
_MATCH_RPC_THRESHOLD_PARAM = os.getenv("SUPABASE_MATCH_RPC_THRESHOLD_PARAM", "match_threshold")
DEFAULT_MATCH_THRESHOLD = float(os.getenv("SUPABASE_MATCH_THRESHOLD", "1.0"))

_PROFILES_TABLE = os.getenv("SUPABASE_PROFILES_TABLE", "profiles")
_ID_COL = os.getenv("SUPABASE_PROFILES_ID_COLUMN", "id")
_DIM = 20

_MEMORIES_TABLE = os.getenv("SUPABASE_USER_MEMORIES_TABLE", "user_memories")
_MATCH_MEMORIES_RPC = os.getenv("SUPABASE_MATCH_USER_MEMORIES_RPC", "match_user_memories")
_RPC_MEM_USER_PARAM = os.getenv("SUPABASE_MATCH_MEMORIES_USER_PARAM", "p_user_id")
_RPC_MEM_QUERY_PARAM = os.getenv("SUPABASE_MATCH_MEMORIES_QUERY_PARAM", "p_query_embedding")
_RPC_MEM_COUNT_PARAM = os.getenv("SUPABASE_MATCH_MEMORIES_COUNT_PARAM", "match_count")

_STORIES_TABLE = os.getenv("SUPABASE_STORIES_TABLE", "stories")
# 與 sql/stories.sql 之 Storage bucket `stories` 對齊；可經 SUPABASE_STORY_IMAGE_BUCKET 覆寫
_STORY_DEFAULT_BUCKET = os.getenv("SUPABASE_STORY_IMAGE_BUCKET", "stories")
_UNLOCKS_TABLE = os.getenv("SUPABASE_USER_UNLOCKS_TABLE", "user_unlocks")

# 寫入 stories 時 PostgREST 需帶入使用者 JWT；clients 建議用 anon public key（非 service_role）以正確套用 RLS


def _normalize_url(raw: str) -> str:
    s = (raw or "").strip().rstrip("/")
    if "/rest" in s:
        s = s.split("/rest")[0].rstrip("/")
    return s


def to_pgvector(vec: list[float]) -> str:
    """將數值向量轉為 pgvector literal。"""
    return "[" + ",".join(str(float(x)) for x in vec) + "]"


def pg_vector_literal(user_vector: list) -> str:
    """PostgreSQL / pgvector 文字格式（相容別名）。"""
    return to_pgvector(user_vector)


@lru_cache(maxsize=1)
def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY")
    return create_client(_normalize_url(url), key)


def auth_sign_in_email_password(email: str, password: str) -> dict[str, Any]:
    """
    Email + 密碼登入（使用專案 `get_client()` 之 anon/service key 連至 GoTrue）。
    回傳 access_token、refresh_token、user_id；供 Reflex 寫入 Session / LocalStorage。
    """
    email = (email or "").strip()
    if not email or not password:
        raise ValueError("email 與 password 不可為空")
    c = get_client()
    res = c.auth.sign_in_with_password({"email": email, "password": password})
    if res.session is None:
        raise RuntimeError("登入失敗：無 session")
    s = res.session
    return {
        "access_token": s.access_token,
        "refresh_token": s.refresh_token,
        "user_id": str(s.user.id),
    }


def auth_sign_up_email_password(email: str, password: str) -> dict[str, Any]:
    """註冊；若專案要求信箱驗證，可能無 session，此時回傳需確認信或丟出說明。"""
    email = (email or "").strip()
    if not email or not password:
        raise ValueError("email 與 password 不可為空")
    c = get_client()
    res = c.auth.sign_up({"email": email, "password": password})
    if res.session is None:
        msg = getattr(res, "message", None) or "註冊已送出，若啟用信箱驗證請至郵件點擊連結後再登入"
        raise LookupError(str(msg))
    s = res.session
    return {
        "access_token": s.access_token,
        "refresh_token": s.refresh_token,
        "user_id": str(s.user.id),
    }


def user_id_from_access_token(access_token: str | None) -> str | None:
    """
    以 GoTrue 驗證 access_token，回傳 auth.users.id（與 public.profiles.id 對齊）。
    失敗或空字串則回傳 None。
    """
    if not access_token or not str(access_token).strip():
        return None
    try:
        resp = get_client().auth.get_user(str(access_token).strip())
        if resp is None:
            return None
        u = getattr(resp, "user", None)
        if u is None:
            return None
        return str(u.id)
    except Exception:
        return None


def resolve_user_id(*, access_token: str | None = None) -> str | None:
    """
    應用層使用者 id 解析順序：
    1) 有效 access_token（Supabase Auth）
    2) 環境變數 MOCK_LOGIN_USER_ID（本機模擬登入）
    3) 環境變數 DB_TEST_PROFILE_ID（僅遷移期與舊測試相容；新功能應優先 token）
    """
    uid = user_id_from_access_token(access_token)
    if uid:
        return uid
    for key in ("MOCK_LOGIN_USER_ID", "DB_TEST_PROFILE_ID"):
        v = (os.getenv(key) or "").strip()
        if v:
            return v
    return None


def get_user_scoped_client(access_token: str) -> Client:
    """
    建立 PostgREST Authorization = Bearer(access_token) 的 Client。
    apikey 使用 SUPABASE_ANON_KEY（若缺則退回 SUPABASE_KEY；若以 service_role，RLS 可能被繞過）。
    """
    url = os.getenv("SUPABASE_URL")
    if not url:
        raise RuntimeError("Missing SUPABASE_URL")
    anon = (os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY") or "").strip()
    if not anon:
        raise RuntimeError("Missing SUPABASE_ANON_KEY or SUPABASE_KEY")
    c = create_client(_normalize_url(url), anon)
    c.postgrest.auth(str(access_token).strip())
    return c


def story_image_object_path(user_id: str, filename: str) -> str:
    """Storage object path：`{user_id}/{basename}`（防止路徑穿越）。"""
    base = Path(str(filename).replace("\\", "/")).name
    base = re.sub(r"[^\w.\-]", "_", base) or "image.png"
    return f"{user_id}/{base}"


def upload_to_supabase_storage(
    access_token: str,
    object_path: str,
    file: Union[bytes, BinaryIO],
    *,
    bucket: str | None = None,
    content_type: str | None = None,
) -> Any:
    """
    以使用者 JWT 上傳至 Storage（須通過 Storage RLS）。
    object_path 必須為 `{user_id}/{filename}`，且 user_id 須與 token 一致。
    """
    uid = user_id_from_access_token(access_token)
    if not uid:
        raise ValueError("無效的 access_token，無法解析 user id")
    if not object_path.startswith(f"{uid}/"):
        raise ValueError("object_path 必須嚴格為 {user_id}/{filename}")

    bkt = bucket if bucket is not None else _STORY_DEFAULT_BUCKET
    payload: bytes | BinaryIO
    if isinstance(file, bytes):
        payload = file
    else:
        payload = file

    file_options: dict[str, str] = {"upsert": "true"}
    if content_type:
        file_options["content-type"] = content_type

    cli = get_user_scoped_client(access_token)
    return cli.storage.from_(bkt).upload(object_path, payload, file_options=file_options)


def list_story_storage_objects(
    access_token: str,
    folder_prefix: str,
    *,
    bucket: str | None = None,
) -> list[dict[str, Any]]:
    """列出 bucket 內某前綴（通常為 `user_id`）底下的物件，供測試／除錯。"""
    bkt = bucket if bucket is not None else _STORY_DEFAULT_BUCKET
    cli = get_user_scoped_client(access_token)
    res = cli.storage.from_(bkt).list(folder_prefix)
    return list(res) if isinstance(res, list) else []


def create_story(
    *,
    access_token: str,
    title: str | None = None,
    body: str | None = None,
    image_object_path: str | None = None,
    image_bucket: str | None = None,
    status: str = "draft",
    sort_order: int = 0,
) -> object:
    """以使用者 JWT 插入 stories（須通過 RLS）。"""
    uid = user_id_from_access_token(access_token)
    if not uid:
        raise ValueError("無效的 access_token，無法解析 user id")

    bucket = image_bucket if image_bucket is not None else _STORY_DEFAULT_BUCKET
    row: dict[str, Any] = {
        "user_id": uid,
        "title": (title or "").strip() or None,
        "body": (body or "").strip() or None,
        "image_object_path": image_object_path,
        "image_bucket": bucket,
        "status": status,
        "sort_order": int(sort_order),
    }

    def _op():
        cli = get_user_scoped_client(access_token)
        return cli.table(_STORIES_TABLE).insert(row).execute()

    return _retry_on_stale_schema(_op)


def default_profile_placeholder_vector() -> list[float]:
    """新使用者／發 Story 前 placeholder：`profiles` 向量先設為全 0.5（二十維）。"""
    return [0.5] * _DIM


def ensure_user_profile(access_token: str) -> None:
    """
    保證 JWT 對應使用者在 `profiles` 有一列：以 **UPSERT**、`ignore_duplicates=True`
    達成「無列則插入全 0.5×20 向量；已存在則不覆寫」。
    須通過 profiles RLS（見 sql/profiles_rls.sql：`INSERT`/`UPDATE` 限 `auth.uid() = id`）。
    """
    uid = user_id_from_access_token(access_token)
    if not uid:
        raise ValueError("無效的 access_token，無法解析 user id")

    cli = get_user_scoped_client(access_token)
    row: dict[str, Any] = {
        _ID_COL: uid,
        _VECTOR_COL: pg_vector_literal(default_profile_placeholder_vector()),
    }

    def _upsert():
        return (
            cli.table(_PROFILES_TABLE)
            .upsert(
                row,
                on_conflict=_ID_COL,
                ignore_duplicates=True,
                returning=ReturnMethod.minimal,
            )
            .execute()
        )

    _retry_on_stale_schema(_upsert)


def ensure_profile_exists(access_token: str) -> None:
    """向後相容別名，等同 `ensure_user_profile`。"""
    ensure_user_profile(access_token)


def upsert_user_vector(access_token: str, user_vector: list[float]) -> object:
    """
    以 JWT 將目前使用者向量寫入 profiles（存在則更新，不存在則建立）。
    內含 `id` 衝突鍵 UPSERT，避免僅 UPDATE 導致新用戶 0 rows。
    """
    if len(user_vector) != _DIM:
        raise ValueError(f"vector must have length {_DIM}, got {len(user_vector)}")
    uid = user_id_from_access_token(access_token)
    if not uid:
        raise ValueError("無效的 access_token，無法解析 user id")

    cli = get_user_scoped_client(access_token)
    row: dict[str, Any] = {
        _ID_COL: uid,
        _VECTOR_COL: pg_vector_literal(user_vector),
    }

    def _upsert():
        return (
            cli.table(_PROFILES_TABLE)
            .upsert(
                row,
                on_conflict=_ID_COL,
                ignore_duplicates=False,
                returning=ReturnMethod.minimal,
            )
            .execute()
        )

    return _retry_on_stale_schema(_upsert)


def upsert_profile_vector_for_user_id(user_id: str, user_vector: list[float]) -> object:
    """
    測試/seed 用：以 service key 直接 UPSERT 指定 user_id 的 profile 向量。
    """
    if len(user_vector) != _DIM:
        raise ValueError(f"vector must have length {_DIM}, got {len(user_vector)}")
    uid = str(user_id).strip()
    if not uid:
        raise ValueError("user_id 不可為空")
    row: dict[str, Any] = {
        _ID_COL: uid,
        _VECTOR_COL: pg_vector_literal(user_vector),
    }

    def _upsert():
        c = get_client()
        return (
            c.table(_PROFILES_TABLE)
            .upsert(
                row,
                on_conflict=_ID_COL,
                ignore_duplicates=False,
                returning=ReturnMethod.minimal,
            )
            .execute()
        )

    return _retry_on_stale_schema(_upsert)


def get_user_stories(access_token: str) -> list[dict[str, Any]]:
    """列出目前 JWT 對應使用者之 stories。"""
    uid = user_id_from_access_token(access_token)
    if not uid:
        raise ValueError("無效的 access_token，無法解析 user id")

    def _op():
        cli = get_user_scoped_client(access_token)
        return (
            cli.table(_STORIES_TABLE)
            .select("*")
            .eq("user_id", uid)
            .order("created_at", desc=True)
            .execute()
        )

    res = _retry_on_stale_schema(_op)
    return list(getattr(res, "data", None) or [])


def _retry_on_stale_schema(fn, *, attempts: int = 6, base_delay: float = 0.4) -> object:
    """
    PostgREST 在新建表／RPC 後可能短暫回 PGRST205（schema cache），
    清快取並遞延重試，避免測試與聯調剛執行 SQL 後立刻失敗。
    """
    last: Optional[Exception] = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as exc:
            last = exc
            code = ""
            try:
                from postgrest.exceptions import APIError

                if isinstance(exc, APIError) and exc.args and isinstance(exc.args[0], dict):
                    code = str(exc.args[0].get("code", "") or "")
            except ImportError:
                pass
            if code in ("PGRST205", "PGRST204") and i < attempts - 1:
                get_client.cache_clear()
                time.sleep(base_delay * (1.0 + 0.2 * i))
                continue
            raise exc
    assert last is not None
    raise last


def ping_user_memories_table() -> None:
    """輕量觸達 user_memories，促進 schema cache 就緒（失敗則忽略）。"""
    try:

        def _op():
            return (
                get_client()
                .table(_MEMORIES_TABLE)
                .select("id")
                .limit(1)
                .execute()
            )

        _retry_on_stale_schema(_op, attempts=4, base_delay=0.25)
    except Exception:
        pass


def update_user_vector(user_id: str, user_vector: list) -> object:
    if len(user_vector) != _DIM:
        raise ValueError(f"vector must have length {_DIM}, got {len(user_vector)}")
    client = get_client()
    return (
        client.table(_PROFILES_TABLE)
        .update({_VECTOR_COL: pg_vector_literal(user_vector)})
        .eq(_ID_COL, str(user_id))
        .execute()
    )


def parse_vector_value(raw: object) -> list[float]:
    """公開給測試／除錯：將 API 回傳的向量欄位轉成 list[float]。"""
    return _parse_stored_vector(raw)


def _parse_stored_vector(raw: object) -> list[float]:
    """將 PostgREST 回傳的 vector（list 或字串）轉成 list[float]。"""
    if raw is None:
        raise ValueError("資料列缺少向量欄位")
    if isinstance(raw, list):
        return [float(x) for x in raw]
    if isinstance(raw, str):
        s = raw.strip()
        if s.startswith("["):
            parsed = ast.literal_eval(s)
            if isinstance(parsed, list):
                return [float(x) for x in parsed]
        parts = [p.strip() for p in s.strip("[]").split(",") if p.strip()]
        return [float(x) for x in parts]
    raise TypeError(f"無法解析向量型別：{type(raw).__name__}")


def get_user_vector(user_id: str) -> list[float]:
    """讀取指定 profile 的向量欄位（與 update 使用相同表／欄位設定）。"""
    client = get_client()
    res = (
        client.table(_PROFILES_TABLE)
        .select(_VECTOR_COL)
        .eq(_ID_COL, str(user_id))
        .limit(1)
        .execute()
    )
    rows = getattr(res, "data", None) or []
    if not rows:
        raise LookupError(f"找不到 id={user_id!r} 的 {_PROFILES_TABLE} 資料列")
    return _parse_stored_vector(rows[0].get(_VECTOR_COL))


def get_profile_vector_via_token(access_token: str) -> list[float] | None:
    """以 JWT 讀取自己 profile 之向量欄位；無列或無欄位回傳 None。"""
    uid = user_id_from_access_token(access_token)
    if not uid:
        return None
    cli = get_user_scoped_client(access_token)

    def _op():
        return cli.table(_PROFILES_TABLE).select(_VECTOR_COL).eq(_ID_COL, uid).limit(1).execute()

    try:
        res = _retry_on_stale_schema(_op)
    except Exception:
        return None
    rows = getattr(res, "data", None) or []
    if not rows:
        return None
    raw = rows[0].get(_VECTOR_COL)
    if raw is None:
        return None
    try:
        return _parse_stored_vector(raw)
    except Exception:
        return None


def profile_has_custom_vector(access_token: str) -> bool:
    """
    是否已建立「非占位」向量：與 ensure_user_profile 預設全 0.5 比對，
    任一維差異 > 1e-3 視為已完成測驗／已寫入自訂向量 → 導向配對牆。
    """
    vec = get_profile_vector_via_token(access_token)
    if vec is None or len(vec) != _DIM:
        return False
    ph = default_profile_placeholder_vector()
    return any(abs(vec[i] - ph[i]) > 1e-3 for i in range(_DIM))


def create_unlock(access_token: str, target_user_id: str) -> object:
    """
    記錄使用者對 target 的解鎖請求（最小 INSERT）。
    若設 MOCK_UNLOCK=1 則不落庫（Task 9 占位）。
    """
    if (os.getenv("MOCK_UNLOCK") or "").strip() in ("1", "true", "yes"):
        return {"mock": True}

    uid = user_id_from_access_token(access_token)
    if not uid:
        raise ValueError("無效的 access_token，無法解析 user id")
    tid = str(target_user_id).strip()
    if not tid:
        raise ValueError("target_user_id 不可為空")
    if tid == uid:
        raise ValueError("不可對自己解鎖")

    row: dict[str, Any] = {"user_id": uid, "target_id": tid}

    def _op():
        cli = get_user_scoped_client(access_token)
        return cli.table(_UNLOCKS_TABLE).insert(row).execute()

    return _retry_on_stale_schema(_op)


def insert_user_memory(user_id: str, summary: str, embedding: list[float]) -> object:
    """寫入一條對話／摘要記憶與 20 維向量（user_memories）。"""
    if len(embedding) != _DIM:
        raise ValueError(f"embedding 必須長度 {_DIM}")

    def _op():
        c = get_client()
        return (
            c.table(_MEMORIES_TABLE)
            .insert(
                {
                    "user_id": str(user_id),
                    "summary": summary.strip(),
                    "embedding": pg_vector_literal(embedding),
                }
            )
            .execute()
        )

    return _retry_on_stale_schema(_op)


def match_user_memories(
    user_id: str,
    query_vector: list[float],
    *,
    match_count: int = 5,
) -> object:
    """呼叫 RPC 依向量相似度取回該使用者之記憶列。"""
    if len(query_vector) != _DIM:
        raise ValueError(f"query_vector 必須長度 {_DIM}")
    payload = {
        _RPC_MEM_USER_PARAM: str(user_id),
        _RPC_MEM_QUERY_PARAM: pg_vector_literal(query_vector),
        _RPC_MEM_COUNT_PARAM: int(match_count),
    }

    def _op():
        c = get_client()
        return c.rpc(_MATCH_MEMORIES_RPC, payload).execute()

    return _retry_on_stale_schema(_op)


def get_matches(user_vector: list, *, match_threshold: float | None = None) -> object:
    if len(user_vector) != _DIM:
        raise ValueError(f"vector must have length {_DIM}, got {len(user_vector)}")
    client = get_client()
    query_vector = to_pgvector(user_vector)
    print(f"DEBUG_VECTOR = {query_vector}")
    payload = {_MATCH_RPC_VEC_PARAM: query_vector}
    try:
        return client.rpc(_MATCH_RPC, payload).execute()
    except Exception:
        if _MATCH_RPC != "get_safe_matches":
            raise
        # 相容舊版簽名：get_safe_matches(match_threshold, query_vector)
        thr = DEFAULT_MATCH_THRESHOLD if match_threshold is None else float(match_threshold)
        payload[_MATCH_RPC_THRESHOLD_PARAM] = thr
        return client.rpc(_MATCH_RPC, payload).execute()


def get_safe_matches_current_user(access_token: str) -> list[dict[str, Any]]:
    """以 JWT 讀取 profiles.vector 後呼叫 `get_safe_matches(query_vector vector)`。"""
    query_vec = get_profile_vector_via_token(access_token)
    if query_vec is None:
        raise ValueError("找不到當前使用者 vector")
    query_vector = to_pgvector(query_vec)
    print(f"DEBUG_VECTOR = {query_vector}")

    def _op():
        cli = get_user_scoped_client(access_token)
        try:
            return cli.rpc("get_safe_matches", {"query_vector": query_vector}).execute()
        except Exception:
            # 相容舊版簽名：get_safe_matches(match_threshold, query_vector)
            return cli.rpc(
                "get_safe_matches",
                {"query_vector": query_vector, "match_threshold": DEFAULT_MATCH_THRESHOLD},
            ).execute()

    res = _retry_on_stale_schema(_op)
    return list(getattr(res, "data", None) or [])
