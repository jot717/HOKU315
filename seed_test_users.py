# -*- coding: utf-8 -*-
"""
Task 7 驗收種子資料：

將 **目前 SUPABASE_ACCESS_TOKEN 對應之使用者** 寫入／更新 `profiles.vector`
（`profiles.id` 必須等於 `auth.users.id`，不可用隨機 UUID）。

用法：
  SUPABASE_ACCESS_TOKEN="..." python seed_test_users.py

需求：
  - SUPABASE_URL / SUPABASE_KEY（種子寫入 profiles；建議 service_role 以利 Admin 查 auth.users）
  - SUPABASE_ACCESS_TOKEN（JWT，`sub` = user id）

說明：
  - 以往使用 uuid4 假帳號會違反 FK；現在僅為 **單一真實使用者** 種入占位向量。
  - 若需配對牆多筆候選，請使用多個真實帳號各跑一次本腳本，或其餘由正式註冊流程建立。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import jwt
from dotenv import load_dotenv

_root = Path(__file__).resolve().parent
load_dotenv(_root / ".env", encoding="utf-8-sig")
load_dotenv(encoding="utf-8-sig")


def get_user_id_from_token(token: str) -> str | None:
    """自 JWT payload 讀取 `sub`（不驗證簽章）。"""
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        sub = payload.get("sub")
        if sub is None or str(sub).strip() == "":
            return None
        return str(sub).strip()
    except Exception:
        return None


def auth_user_exists(client, user_id: str, access_token: str) -> bool:
    """
    確認 user_id 存在於 auth 使用者庫。
    優先使用 Admin `get_user_by_id`（需具權限之 key）；
    失敗則以帶入之 access_token 呼叫 `get_user` 佐證 sub 與列一致。
    """
    try:
        r = client.auth.admin.get_user_by_id(user_id)
        return getattr(r, "user", None) is not None
    except Exception:
        try:
            r = client.auth.get_user(access_token)
            u = getattr(r, "user", None) if r else None
            return u is not None and str(u.id) == str(user_id)
        except Exception:
            return False


def main() -> int:
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        print("SKIP: SUPABASE_URL / SUPABASE_KEY missing", file=sys.stderr)
        return 0

    token = (os.getenv("SUPABASE_ACCESS_TOKEN") or "").strip()
    if not token:
        print("SKIP: SUPABASE_ACCESS_TOKEN missing", file=sys.stderr)
        return 0

    user_id = get_user_id_from_token(token)
    if not user_id:
        print("SKIP: 無法解析 user_id")
        return 0

    import db_service

    client = db_service.get_client()
    if not auth_user_exists(client, user_id, token):
        print("SKIP: user 不存在於 auth.users")
        return 0

    base = db_service.default_profile_placeholder_vector()
    db_service.upsert_profile_vector_for_user_id(user_id, base)

    n = 1
    print(f"Successfully upserted {n} users")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
