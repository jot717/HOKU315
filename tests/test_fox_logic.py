# -*- coding: utf-8 -*-
"""fox_logic.generate_vector 與 db_service 向量格式相容性測試。"""
from __future__ import annotations

import sys

import db_service
import fox_logic


def _assert_db_service_compatible(vec: list[float]) -> None:
    assert isinstance(vec, list), "must be list[float], not tuple"
    assert len(vec) == db_service._DIM == fox_logic.VECTOR_DIM
    for i, x in enumerate(vec):
        assert isinstance(x, float), f"index {i} must be float, got {type(x).__name__}"
        assert 0.0 <= x <= 1.0, f"index {i} out of range: {x}"


def main() -> int:
    # Sequence path：模擬 20 題滑桿 0..1
    sliders = [i / 19.0 for i in range(20)]
    v1 = fox_logic.generate_vector(sliders)
    _assert_db_service_compatible(v1)
    assert v1 == fox_logic.generate_vector(tuple(sliders))

    # Mapping path：依鍵填滿
    m = {k: 0.25 for k in fox_logic.SOCIAL_MINE_KEYS}
    m["punctuality_mine"] = 0.9
    v2 = fox_logic.generate_vector(m)
    _assert_db_service_compatible(v2)
    assert v2[fox_logic.SOCIAL_MINE_KEYS.index("punctuality_mine")] == 0.9

    # 與 db_service 字串化管線相容（不觸發網路）
    s = db_service.pg_vector_literal(v2)
    assert s.startswith("[") and s.endswith("]")
    assert s.count(",") == 19

    # 錯誤路徑
    try:
        fox_logic.generate_vector([0.5] * 19)
    except ValueError:
        pass
    else:
        print("FAIL: expected ValueError for wrong length", file=sys.stderr)
        return 1

    try:
        fox_logic.generate_vector({k: 0.1 for k in list(fox_logic.SOCIAL_MINE_KEYS)[:10]})
    except KeyError:
        pass
    else:
        print("FAIL: expected KeyError for missing keys", file=sys.stderr)
        return 1

    # 越界輸入被 clamp
    v3 = fox_logic.generate_vector([-1.0, 2.0] + [0.5] * 18)
    assert v3[0] == 0.0 and v3[1] == 1.0

    assert abs(fox_logic.weave_light_mean(v3) - sum(v3[:4]) / 4.0) < 1e-12

    # 狐狸譜系主導：霜鎧組（索引 10–14）顯著偏高
    push_rime = [0.05] * 10 + [0.95] * 5 + [0.05] * 5
    vr = fox_logic.generate_vector(push_rime)
    fox_txt = fox_logic.dominant_fox_message(vr)
    assert "霜鎧" in fox_txt and "北極狐" in fox_txt

    print("OK: fox_logic.generate_vector -> list[float] x20, compatible with db_service._DIM & pg_vector_literal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
