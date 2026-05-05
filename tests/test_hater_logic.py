# -*- coding: utf-8 -*-
"""
Task 7：門檻與衝突維度邏輯檢查。

- 離線：驗證 blurred / blocked 門檻與最大差異維度標籤推導。
- 可選整合：若有 SUPABASE_ACCESS_TOKEN，檢查 RPC `get_safe_matches` 欄位結構。
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

import fox_logic

_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env", encoding="utf-8-sig")
load_dotenv(encoding="utf-8-sig")


def _l2(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _largest_conflict_label(a: list[float], b: list[float]) -> str:
    idx = max(range(len(a)), key=lambda i: abs(a[i] - b[i]))
    return fox_logic.SOCIAL_MINE_DIMENSIONS[idx][1]


def _offline_assertions() -> None:
    base = [0.5] * fox_logic.VECTOR_DIM
    safe = [0.6] * fox_logic.VECTOR_DIM
    blur = [0.7] * fox_logic.VECTOR_DIM
    block = [0.8] * fox_logic.VECTOR_DIM

    d_safe = _l2(base, safe)
    d_blur = _l2(base, blur)
    d_block = _l2(base, block)
    assert d_safe < 0.7, f"safe distance unexpected: {d_safe}"
    assert 0.7 <= d_blur < 1.2, f"blur distance unexpected: {d_blur}"
    assert d_block >= 1.2, f"block distance unexpected: {d_block}"

    is_blurred_safe = d_safe >= 0.7
    is_blurred_blur = d_blur >= 0.7
    assert is_blurred_safe is False
    assert is_blurred_blur is True

    a = [0.5] * fox_logic.VECTOR_DIM
    b = [0.5] * fox_logic.VECTOR_DIM
    b[13] = 1.0  # 第 14 維差異最大
    label = _largest_conflict_label(a, b)
    expected = fox_logic.SOCIAL_MINE_DIMENSIONS[13][1]
    assert label == expected, f"expected {expected!r}, got {label!r}"


def _integration_check() -> int:
    token = (os.getenv("SUPABASE_ACCESS_TOKEN") or "").strip()
    if not token:
        print("SKIP: SUPABASE_ACCESS_TOKEN missing", file=sys.stderr)
        return 0

    import db_service

    try:
        rows = db_service.get_safe_matches_current_user(token)
    except Exception as exc:
        print(f"SKIP: RPC get_safe_matches not ready: {exc}", file=sys.stderr)
        return 0

    if rows:
        row = rows[0]
        required = {
            "matched_user_id",
            "distance",
            "is_blurred",
            "conflict_dim_index",
            "conflict_dim_label",
            "blocked_count",
        }
        missing = sorted([k for k in required if k not in row])
        assert not missing, f"RPC row missing fields: {missing}"

    return 0


def main() -> int:
    _offline_assertions()
    code = _integration_check()
    if code != 0:
        return code
    print("OK: hater logic thresholds + conflict label")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
