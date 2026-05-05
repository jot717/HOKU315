# -*- coding: utf-8 -*-
# 歸檔：階段性整合測試（連線 + update + RPC）。正式流程請用 tests/test_db_connection.py。
from __future__ import annotations

import os
import sys
from pathlib import Path

if sys.platform == "win32":
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError, ValueError):
            pass

from dotenv import load_dotenv

_repo_root = Path(__file__).resolve().parents[1]
load_dotenv(_repo_root / ".env", encoding="utf-8-sig")
load_dotenv(encoding="utf-8-sig")

import db_service

db_service.get_client.cache_clear()

DEFAULT_PROFILE_ID = "00000000-0000-0000-0000-000000000001"


def main() -> int:
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        print("FAIL: missing SUPABASE_URL or SUPABASE_KEY in .env", file=sys.stderr)
        return 1

    profile_id = os.getenv("DB_TEST_PROFILE_ID") or DEFAULT_PROFILE_ID
    fake_vec = [0.1] * 20

    try:
        client = db_service.get_client()
    except Exception as e:
        print(f"FAIL connection: {e}", file=sys.stderr)
        return 1
    print(f"[OK] connection client={type(client).__name__}")

    print(f"[RUN] update profiles id={profile_id} col={db_service._VECTOR_COL!r}")
    try:
        upd = db_service.update_user_vector(profile_id, fake_vec)
        print(f"[OK] update data={upd.data!r}")
    except Exception as e:
        print(f"FAIL update: {e}", file=sys.stderr)
        return 1

    print(f"[RUN] rpc {db_service._MATCH_RPC!r} vec_param={db_service._MATCH_RPC_VEC_PARAM!r}")
    try:
        mat = db_service.get_matches(fake_vec)
        print(f"[OK] rpc data={mat.data!r}")
    except Exception as e:
        print(f"FAIL rpc: {e}", file=sys.stderr)
        return 1

    print("[OK] connection and query succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
