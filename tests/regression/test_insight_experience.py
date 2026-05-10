from __future__ import annotations

from product.insight.experience.insight_formatter import format_emotional_insight


def test_insight_experience() -> None:
    insight = {
        "shared_traits": [
            "music",
            "travel",
        ],
    }

    result = format_emotional_insight(
        insight,
        82.0,
    )

    assert "compatibility_title" in result
    assert "energy_summary" in result
    assert "final_insight" in result
