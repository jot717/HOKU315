import random
from typing import Mapping, Any


def compute_match(user_a: Mapping[str, Any], user_b: Mapping[str, Any]) -> float:
    """
    Minimal rule-based match engine (MVP).

    user_a / user_b:
      - interests: iterable of hashable values
      - activity: numeric (0–10 scale suggested)
    """

    interests_a = set(user_a.get("interests") or [])
    interests_b = set(user_b.get("interests") or [])
    interest_overlap = len(interests_a & interests_b)

    activity_a = float(user_a.get("activity", 0))
    activity_b = float(user_b.get("activity", 0))
    activity_diff = abs(activity_a - activity_b)

    # Normalize activity similarity to 0–10 (clamped), higher is better.
    activity_similarity = max(0.0, 10.0 - activity_diff)

    # Random factor scaled to [0, 10).
    random_component = random.random() * 10.0

    score = (
        interest_overlap * 0.4
        + activity_similarity * 0.3
        + random_component * 0.3
    )

    # Clamp to 0–100 for downstream UI / tests.
    return max(0.0, min(100.0, score))


def evaluate_match(score: float, threshold: float = 70.0) -> str:
    """Return MATCH / NO_MATCH based on a numeric score."""
    return "MATCH" if score >= threshold else "NO_MATCH"

