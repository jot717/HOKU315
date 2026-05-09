from typing import Any, Dict

from .unlock_engine import generate_insight


def run_unlock(match_score: float) -> Dict[str, Any]:
    insight = generate_insight(match_score)

    return {
        "unlock_status": "revealed",
        "insight": insight,
    }
