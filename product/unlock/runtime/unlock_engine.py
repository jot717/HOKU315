from __future__ import annotations

from typing import Any, Dict

from product.insight.runtime.insight_engine import generate_dynamic_insight


def generate_insight(
    user_a: Dict[str, Any],
    user_b: Dict[str, Any],
    match_score: float,
) -> Dict[str, Any]:
    interests_a = user_a.get("interests", [])
    interests_b = user_b.get("interests", [])

    activity_a = float(user_a.get("activity", 0))
    activity_b = float(user_b.get("activity", 0))

    activity_diff = abs(activity_a - activity_b)

    return generate_dynamic_insight(
        interests_a,
        interests_b,
        activity_diff,
        match_score,
    )
