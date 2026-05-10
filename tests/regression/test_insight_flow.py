from __future__ import annotations

from product.unlock.runtime.unlock_flow import run_unlock


def _assert_dynamic_insight() -> None:
    user_a = {
        "interests": ["ai", "music", "travel"],
        "activity": 5,
    }

    user_b = {
        "interests": ["music", "travel", "sports"],
        "activity": 6,
    }

    result = run_unlock(
        user_a,
        user_b,
        82.0,
    )

    insight = result["insight"]

    assert "compatibility_score" in insight
    assert "shared_traits" in insight
    assert "activity_analysis" in insight
    assert "ai_summary" in insight


def test_insight_flow_dynamic_insight() -> None:
    _assert_dynamic_insight()
