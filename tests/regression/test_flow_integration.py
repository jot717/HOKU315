from __future__ import annotations

from product.core.runtime.flow_orchestrator import run_full_flow


def _assert_full_flow() -> None:
    user_a = {
        "interests": ["ai", "music", "travel"],
        "activity": 5,
    }

    user_b = {
        "interests": ["music", "travel", "sports"],
        "activity": 6,
    }

    result = run_full_flow(
        user_a,
        user_b,
    )

    assert "match" in result
    assert "unlock" in result

    unlock = result["unlock"]

    assert unlock["unlock_status"] == "revealed"

    insight = unlock["insight"]

    assert "compatibility_score" in insight
    assert "ai_summary" in insight


def test_full_flow() -> None:
    _assert_full_flow()
