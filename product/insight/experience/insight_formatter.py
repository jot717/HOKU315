from __future__ import annotations

from typing import Any, Dict


def format_emotional_insight(
    insight: Dict[str, Any],
    score: float,
) -> Dict[str, str]:
    if score >= 80:
        compatibility = "Exceptional Compatibility"
        energy = (
            "You naturally amplify each other's energy."
        )

    elif score >= 60:
        compatibility = "Strong Potential"
        energy = (
            "You share meaningful overlap with different strengths."
        )

    else:
        compatibility = "Unexpected Dynamic"
        energy = (
            "Your differences may create interesting tension."
        )

    traits = insight.get(
        "shared_traits",
        [],
    )

    traits_text = ", ".join(str(t) for t in traits)

    final_insight = (
        f"You both connect through {traits_text}. "
        "The interaction feels naturally balanced."
    )

    return {
        "compatibility_title": compatibility,
        "energy_summary": energy,
        "final_insight": final_insight,
    }
