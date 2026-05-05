# -*- coding: utf-8 -*-
"""
Task 6：以 1×1 PNG 實傳 Storage，並 list 驗證路徑為 `{user_id}/{filename}`。

需：SUPABASE_URL、SUPABASE_KEY（供 get_user）、SUPABASE_ANON_KEY 或同 anon、
   SUPABASE_ACCESS_TOKEN、且 Supabase 已執行 sql/stories.sql（bucket `stories` + Storage RLS）。
"""
from __future__ import annotations

import base64
import os
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv

_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env", encoding="utf-8-sig")
load_dotenv(encoding="utf-8-sig")

# 最小有效 1×1 PNG（透明像素）
_PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAosB7pWvS8sAAAAASUVORK5CYII="
)


def main() -> int:
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        print("SKIP: SUPABASE_URL / SUPABASE_KEY missing", file=sys.stderr)
        return 0

    token = (os.getenv("SUPABASE_ACCESS_TOKEN") or "").strip()
    if not token:
        print("SKIP: SUPABASE_ACCESS_TOKEN missing", file=sys.stderr)
        return 0

    import db_service

    db_service.get_client.cache_clear()

    uid = db_service.user_id_from_access_token(token)
    if not uid:
        print("SKIP: cannot resolve user id from token", file=sys.stderr)
        return 0

    fname = f"pytest_1x1_{uuid.uuid4().hex[:8]}.png"
    path = db_service.story_image_object_path(uid, fname)
    if not path.startswith(f"{uid}/"):
        print(f"FAIL: bad path {path!r}", file=sys.stderr)
        return 1

    try:
        db_service.upload_to_supabase_storage(
            token,
            path,
            _PNG_1X1,
            content_type="image/png",
        )
    except Exception as exc:
        print(f"SKIP: upload failed: {exc}", file=sys.stderr)
        return 0

    try:
        rows = db_service.list_story_storage_objects(token, uid)
    except Exception as exc:
        print(f"SKIP: list failed: {exc}", file=sys.stderr)
        return 0

    names = [r.get("name") for r in rows if isinstance(r, dict)]
    if fname not in names:
        print(f"FAIL: file {fname!r} not in list {names!r}", file=sys.stderr)
        return 1

    print(f"OK: story_storage bucket=stories path={path} listed=yes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
