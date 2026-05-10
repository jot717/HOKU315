from __future__ import annotations

from typing import Any, Dict


def build_reveal_state(
    insight: Dict[str, Any],
    score: float,
) -> Dict[str, Any]:
    _ = insight  # reserved for tiered copy / traits in later UX
    if score >= 80:
        level = "HIGH"
        reveal_delay = 0.5

    elif score >= 60:
        level = "MEDIUM"
        reveal_delay = 1.0

    else:
        level = "LOW"
        reveal_delay = 1.5

    return {
        "level": level,
        "reveal_delay": reveal_delay,
        "show_meter": True,
        "show_final_card": score >= 60,
    }
