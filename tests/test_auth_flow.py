# -*- coding: utf-8 -*-
"""
Task 6.5：登入 → access_token → Session（LocalStorage）管線之可重現驗證。

離線／無憑證：
  - 仍檢查 Reflex 頁面模組可匯入、`SessionState` 具 persist 欄位、`login_page` 可編譯。
整合（可選）：
  - 設定環境變數 `AUTH_TEST_EMAIL`、`AUTH_TEST_PASSWORD`（及既有 `SUPABASE_URL`、`SUPABASE_KEY`）
    時，呼叫 `auth_sign_in_email_password`，斷言 token 可經 `user_id_from_access_token` 解析。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env", encoding="utf-8-sig")
load_dotenv(encoding="utf-8-sig")


def _smoke_imports() -> None:
    from fox_quiz import login_page as lp
    from fox_quiz import story_page as sp
    from fox_quiz.session_state import SessionState

    assert lp.login_page is not None
    assert sp.story_page is not None
    fields = SessionState.get_fields()
    assert "access_token" in fields and "refresh_token" in fields


def _integration_sign_in() -> int:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    email = (os.getenv("AUTH_TEST_EMAIL") or "").strip()
    password = os.getenv("AUTH_TEST_PASSWORD") or ""

    if not url or not key:
        print("SKIP: integration — SUPABASE_URL / SUPABASE_KEY missing", file=sys.stderr)
        return 0
    if not email or not password:
        print(
            "SKIP: integration — set AUTH_TEST_EMAIL + AUTH_TEST_PASSWORD for live login test",
            file=sys.stderr,
        )
        return 0

    import db_service

    db_service.get_client.cache_clear()
    data = db_service.auth_sign_in_email_password(email, password)
    token = (data.get("access_token") or "").strip()
    if not token:
        print("FAIL: sign_in returned empty access_token", file=sys.stderr)
        return 1
    uid = db_service.user_id_from_access_token(token)
    if not uid:
        print("FAIL: user_id_from_access_token failed after sign_in", file=sys.stderr)
        return 1
    if data.get("user_id") and str(data["user_id"]) != str(uid):
        print("FAIL: user_id mismatch between session and get_user", file=sys.stderr)
        return 1

    print(f"OK: auth_flow sign_in → token ok, uid={uid[:8]}…")
    return 0


def main() -> int:
    try:
        _smoke_imports()
    except Exception as e:
        print(f"FAIL: smoke import: {e}", file=sys.stderr)
        return 1

    from fox_quiz import fox_quiz as fq

    assert fq.app is not None

    code = _integration_sign_in()
    if code != 0:
        return code

    print("OK: test_auth_flow smoke + optional integration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
