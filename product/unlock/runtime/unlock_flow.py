from __future__ import annotations

from typing import Any, Dict

from .unlock_engine import generate_insight


def run_unlock(
    user_a: Dict[str, Any],
    user_b: Dict[str, Any],
    match_score: float,
) -> Dict[str, Any]:
    insight = generate_insight(
        user_a,
        user_b,
        match_score,
    )

    return {
        "unlock_status": "revealed",
        "insight": insight,
    }
