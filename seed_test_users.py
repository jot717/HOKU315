# -*- coding: utf-8 -*-
"""
Task 7 驗收種子資料：
建立 3~5 個測試 profiles 向量，覆蓋 Safe / Blurred / Blocked 區間。

用法：
  python seed_test_users.py

需求：
  - SUPABASE_URL / SUPABASE_KEY
  - SUPABASE_ACCESS_TOKEN（作為 current user 參考向量）
"""
from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv

_root = Path(__file__).resolve().parent
load_dotenv(_root / ".env", encoding="utf-8-sig")
load_dotenv(encoding="utf-8-sig")


def _clamp01(v: float) -> float:
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def _offset(vec: list[float], delta: float) -> list[float]:
    return [_clamp01(x + delta) for x in vec]


def main() -> int:
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        print("SKIP: SUPABASE_URL / SUPABASE_KEY missing", file=sys.stderr)
        return 0

    token = (os.getenv("SUPABASE_ACCESS_TOKEN") or "").strip()
    if not token:
        print("SKIP: SUPABASE_ACCESS_TOKEN missing", file=sys.stderr)
        return 0

    import db_service

    uid = db_service.user_id_from_access_token(token)
    if not uid:
        print("SKIP: 無法由 SUPABASE_ACCESS_TOKEN 解析 user id", file=sys.stderr)
        return 0

    base = db_service.default_profile_placeholder_vector()
    # 對應 L2 距離約：0.00、0.45（safe）、0.89（blurred）、1.34（blocked）、1.79（blocked+）
    seeds: list[tuple[str, list[float]]] = [
        ("self_base", base),
        ("safe", _offset(base, 0.10)),
        ("blurred", _offset(base, 0.20)),
        ("blocked", _offset(base, 0.30)),
        ("blocked_high", _offset(base, 0.40)),
    ]

    db_service.upsert_profile_vector_for_user_id(uid, base)

    created: list[tuple[str, str]] = [("self", uid)]
    for tag, vec in seeds[1:]:
        fake_uid = str(uuid.uuid4())
        db_service.upsert_profile_vector_for_user_id(fake_uid, vec)
        created.append((tag, fake_uid))

    print("OK: seeded test users")
    for tag, sid in created:
        print(f"  - {tag}: {sid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
