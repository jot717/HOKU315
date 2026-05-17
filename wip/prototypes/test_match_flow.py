from __future__ import annotations

from product.match.runtime.match_engine import compute_match, evaluate_match


def test_match_flow_basic_range() -> None:
    user_a = {
        "interests": ["music", "ai", "travel"],
        "activity": 5,
    }
    user_b = {
        "interests": ["music", "sports"],
        "activity": 6,
    }

    score = compute_match(user_a, user_b)
    result = evaluate_match(score)

    assert 0.0 <= score <= 100.0
    assert result in {"MATCH", "NO_MATCH"}

