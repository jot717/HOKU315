from __future__ import annotations

from typing import Any, Dict

from product.match.runtime.match_flow import run_match
from product.unlock.runtime.unlock_flow import run_unlock


def run_full_flow(
    user_a: Dict[str, Any],
    user_b: Dict[str, Any],
) -> Dict[str, Any]:
    match_result = run_match(user_a, user_b)

    score = match_result["score"]

    unlock_result = run_unlock(
        user_a,
        user_b,
        score,
    )

    return {
        "match": match_result,
        "unlock": unlock_result,
    }
