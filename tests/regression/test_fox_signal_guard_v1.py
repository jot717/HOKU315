from __future__ import annotations

from pathlib import Path

from fox_quiz.ui.insight_panel import insight_panel
from product.guard.runtime.signal_guard_engine import evaluate_signal_risk

ROOT = Path(__file__).resolve().parents[2]


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


def test_archived_signal_guard_card_exists() -> None:
    p = ROOT / "docs/archive/dead_components_reference/signal_guard_card.py"
    assert p.is_file()


def test_insight_panel_compiles() -> None:
    assert insight_panel() is not None
