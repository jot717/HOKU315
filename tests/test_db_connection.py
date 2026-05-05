# -*- coding: utf-8 -*-
"""正式測試：Supabase 連線與 RPC get_safe_matches（需 .env）。僅在 __main__ 執行，避免 pytest 匯入時打 API。"""
from __future__ import annotations

import os
import sys
from pathlib import Path

if sys.platform == "win32":
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError, ValueError):
            pass

from dotenv import load_dotenv


def main() -> int:
    _repo_root = Path(__file__).resolve().parent.parent
    load_dotenv(_repo_root / ".env", encoding="utf-8-sig")
    load_dotenv(encoding="utf-8-sig")

    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        print(
            "SKIP: SUPABASE_URL / SUPABASE_KEY 未設定（離線／Mock 模式不跑 E2E 連線）。",
            file=sys.stderr,
        )
        return 0

    import db_service

    db_service.get_client.cache_clear()

    fake = [0.1] * 20

    _ = db_service.get_client()
    print("[OK] connection")

    db_service.get_matches(fake)
    print("OK RPC get_safe_matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
