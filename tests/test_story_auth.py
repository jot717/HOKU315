# -*- coding: utf-8 -*-
"""
Task 6：在模擬登入（SUPABASE_ACCESS_TOKEN）下寫入 stories，並驗證 object path 為 `user_id/檔名`。

需：SUPABASE_URL、可解析 JWT 之金鑰（SUPABASE_KEY，供 get_user）、
   stories 表已建、profiles 有該 user 之列、
   寫入 RLS 建議使用 SUPABASE_ANON_KEY + 使用者 JWT（若僅有 service_role 則 RLS 可能繞過，仍測路徑規範）。

無 token 或無法連線：SKIP exit 0。
"""
from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv

_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env", encoding="utf-8-sig")
load_dotenv(encoding="utf-8-sig")


def main() -> int:
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        print("SKIP: SUPABASE_URL / SUPABASE_KEY missing", file=sys.stderr)
        return 0

    token = (os.getenv("SUPABASE_ACCESS_TOKEN") or "").strip()
    if not token:
        print(
            "SKIP: SUPABASE_ACCESS_TOKEN missing（模擬登入請貼上使用者 access_token）",
            file=sys.stderr,
        )
        return 0

    import db_service

    db_service.get_client.cache_clear()

    uid = db_service.user_id_from_access_token(token)
    if not uid:
        print("SKIP: access_token 無法解析為 user id", file=sys.stderr)
        return 0

    fname = f"jot_story_{uuid.uuid4().hex[:8]}.png"
    path = db_service.story_image_object_path(uid, fname)
    if not path.startswith(f"{uid}/"):
        print(f"FAIL: path prefix mismatch: {path!r}", file=sys.stderr)
        return 1

    title = f"[pytest] story auth {fname}"

    try:
        db_service.create_story(
            access_token=token,
            title=title,
            body="integration body",
            image_object_path=path,
        )
    except Exception as exc:
        print(f"SKIP or FAIL insert: {exc}", file=sys.stderr)
        return 0

    rows = db_service.get_user_stories(token)
    match = [r for r in rows if isinstance(r, dict) and r.get("title") == title]
    if not match:
        print("FAIL: inserted story not found in get_user_stories", file=sys.stderr)
        return 1

    stored_path = match[0].get("image_object_path") or ""
    if stored_path != path or not stored_path.startswith(f"{uid}/"):
        print(f"FAIL: bad image_object_path in row: {stored_path!r}", file=sys.stderr)
        return 1

    print(f"OK: story_auth uid={uid[:8]}… path={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
