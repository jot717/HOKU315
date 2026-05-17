from __future__ import annotations

from typing import Mapping, Any, Dict

from .match_engine import compute_match, evaluate_match


def run_match(user_a: Mapping[str, Any], user_b: Mapping[str, Any]) -> Dict[str, Any]:
    """End-to-end MATCH FLOW v1 runtime helper (score + decision)."""
    score = compute_match(user_a, user_b)
    result = evaluate_match(score)
    return {
        "score": score,
        "result": result,
    }

