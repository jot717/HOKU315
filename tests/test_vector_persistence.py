# -*- coding: utf-8 -*-
"""
向量落地：fox_logic 產生向量 -> db_service 寫入 -> get_user_vector 讀回斷言一致。

若 profiles 無該 id 或無法讀回，則 SKIP（exit 0）並提示設定 DB_TEST_PROFILE_ID。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env", encoding="utf-8-sig")
load_dotenv(encoding="utf-8-sig")

import db_service
import fox_logic


def _close(a: list[float], b: list[float], tol: float = 1e-4) -> bool:
    if len(a) != len(b):
        return False
    return all(abs(x - y) <= tol for x, y in zip(a, b, strict=True))


def main() -> int:
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        print("SKIP: missing SUPABASE_URL / SUPABASE_KEY", file=sys.stderr)
        return 0

    db_service.get_client.cache_clear()

    uid = os.getenv("DB_TEST_PROFILE_ID", "00000000-0000-0000-0000-000000000001")
    sliders = [((i * 7 + 3) % 100) / 100.0 for i in range(fox_logic.VECTOR_DIM)]
    vec = fox_logic.generate_vector(sliders)

    db_service.update_user_vector(uid, vec)
    try:
        read_back = db_service.get_user_vector(uid)
    except LookupError:
        print(
            "SKIP: 無法讀回向量（profiles 無此 id 或更新 0 列）。"
            "請設定與 Supabase 既有 profile 一致之 DB_TEST_PROFILE_ID。",
            file=sys.stderr,
        )
        return 0

    if not _close(vec, read_back, tol=1e-4):
        print(f"FAIL: written != read\n  w={vec}\n  r={read_back}", file=sys.stderr)
        return 1

    print("OK: vector round-trip via db_service.update_user_vector + get_user_vector")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
