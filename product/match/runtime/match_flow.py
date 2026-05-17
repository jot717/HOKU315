from __future__ import annotations

from typing import Any, Dict, Mapping


def run_match(user_a: Mapping[str, Any], user_b: Mapping[str, Any]) -> Dict[str, Any]:
    """Minimal MATCH FLOW helper for flow_orchestrator (Phase1 stub)."""
    interests_a = set(user_a.get("interests") or [])
    interests_b = set(user_b.get("interests") or [])
    overlap = len(interests_a & interests_b)
    score = min(100.0, max(0.0, 40.0 + overlap * 15.0))
    result = "MATCH" if score >= 50.0 else "NO_MATCH"
    return {"score": score, "result": result}
