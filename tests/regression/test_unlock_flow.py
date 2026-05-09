from __future__ import annotations

from product.unlock.runtime.unlock_flow import run_unlock


def test_unlock_flow() -> None:
    result = run_unlock(82.0)

    assert result["unlock_status"] == "revealed"

    insight = result["insight"]

    assert "compatibility_score" in insight
    assert "shared_traits" in insight
    assert "ai_summary" in insight
