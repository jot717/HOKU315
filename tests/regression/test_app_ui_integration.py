from __future__ import annotations

from product.core.runtime.flow_orchestrator import run_full_flow


def test_ui_flow_runtime() -> None:
    user_a = {
        "interests": ["ai", "music"],
        "activity": 5,
    }

    user_b = {
        "interests": ["music", "travel"],
        "activity": 6,
    }

    result = run_full_flow(
        user_a,
        user_b,
    )

    assert "match" in result
    assert "unlock" in result

    insight = result["unlock"]["insight"]

    assert "ai_summary" in insight
