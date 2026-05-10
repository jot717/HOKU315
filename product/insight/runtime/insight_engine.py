from __future__ import annotations

from typing import Any, Dict, List


def generate_dynamic_insight(
    interests_a: List[str],
    interests_b: List[str],
    activity_diff: float,
    match_score: float,
) -> Dict[str, Any]:
    shared = list(set(interests_a) & set(interests_b))

    if len(shared) >= 3:
        trait = "Strong shared interests"
    elif len(shared) >= 1:
        trait = "Moderate shared interests"
    else:
        trait = "Different personalities"

    if activity_diff <= 2:
        activity_note = "Very similar activity rhythm"
    else:
        activity_note = "Different activity patterns"

    summary = f"{trait}. {activity_note}."

    return {
        "compatibility_score": match_score,
        "shared_traits": shared,
        "activity_analysis": activity_note,
        "ai_summary": summary,
    }
