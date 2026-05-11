from __future__ import annotations

from fox_quiz.ui.components.signal_guard_card import signal_guard_card
from fox_quiz.ui.insight_panel import insight_panel
from product.guard.runtime.signal_guard_engine import evaluate_signal_risk


def test_evaluate_signal_risk_returns_dict() -> None:
    out = evaluate_signal_risk(
        {
            "shared_traits": ["quiet"],
            "activity_analysis": "節奏有些拉扯",
        },
        38.0,
    )
    assert isinstance(out, dict)
    assert "risk_level" in out
    assert "risk_flags" in out
    assert "guardian_action" in out
    assert "guardian_warning" in out


def test_signal_guard_card_and_insight_panel_compile() -> None:
    assert signal_guard_card("medium", ["訊號不穩定"], "可以再觀察一下。") is not None
    assert insight_panel() is not None
