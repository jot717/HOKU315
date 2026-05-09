from typing import Any, Dict


def generate_insight(match_score: float) -> Dict[str, Any]:
    if match_score >= 85:
        summary = "High compatibility detected."
    elif match_score >= 70:
        summary = "Strong compatibility potential."
    else:
        summary = "Moderate compatibility."

    return {
        "compatibility_score": match_score,
        "shared_traits": [
            "curiosity",
            "exploration",
        ],
        "ai_summary": summary,
    }
