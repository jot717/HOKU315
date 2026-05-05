# -*- coding: utf-8 -*-
"""
UI 壓力測試：
1) 單維快速 on_change 等價更新；
2) 每輪 20 維同時變動（模擬多滑桿連續事件）+ generate_vector；
3) 織光維度均值、狐狸譜系 `dominant_fox_message`、高頻 on_change 不卡死。
"""
from __future__ import annotations

import fox_logic
from fox_quiz.fox_quiz import QuizState


def _apply_score_at(scores: list[float], index: int, raw: list[float] | float) -> list[float]:
    """鏡像 QuizState.set_score_at 的數值邏輯（無 Reflex runtime）。"""
    v = QuizState._coerce_slider_value(raw)
    if v < 0.0:
        v = 0.0
    elif v > 1.0:
        v = 1.0
    out = [*scores]
    cur = out[index]
    if abs(cur - v) < 1e-6:
        return out
    out[index] = v
    return out


def main() -> int:
    scores = [0.5] * fox_logic.VECTOR_DIM

    # 階段 A：單維交錯高頻（模擬 on_change 風暴）
    iterations = 20_000
    for step in range(iterations):
        idx = step % fox_logic.VECTOR_DIM
        if step % 3 == 0:
            payload: list[float] | float = [(step % 100) / 100.0]
        elif step % 3 == 1:
            payload = float((step % 57) / 57.0)
        else:
            payload = [float(step % 2)]
        scores = _apply_score_at(scores, idx, payload)
        vec = fox_logic.generate_vector(scores)
        assert len(vec) == fox_logic.VECTOR_DIM
        assert all(isinstance(x, float) for x in vec)

    # 階段 B：每輪 20 維依序瞬刷（模擬多滑桿在同一回合內連續觸發）
    rounds = 4000
    for r in range(rounds):
        for i in range(fox_logic.VECTOR_DIM):
            t = ((r * 7 + i * 3) % 91) / 91.0
            scores = _apply_score_at(scores, i, [t])
        vec = fox_logic.generate_vector(scores)
        assert len(vec) == fox_logic.VECTOR_DIM

    # 織光閾值：高前四維應使均值 > 0.7
    hi = fox_logic.generate_vector([0.88] * fox_logic.VECTOR_DIM)
    assert fox_logic.weave_light_mean(hi) > 0.7
    lo = fox_logic.generate_vector([0.1] * fox_logic.VECTOR_DIM)
    assert fox_logic.weave_light_mean(lo) <= 0.7

    # 狐狸語：霜鎧組主導
    rime_vec = fox_logic.generate_vector([0.05] * 10 + [0.96] * 5 + [0.05] * 5)
    assert "霜鎧" in fox_logic.dominant_fox_message(rime_vec)

    total_ops = iterations + rounds * fox_logic.VECTOR_DIM
    print(
        f"OK: stress single-axis {iterations} ops + "
        f"{rounds} rounds x{fox_logic.VECTOR_DIM} simultaneous dims "
        f"({total_ops} score writes) + generate_vector, no stall"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
