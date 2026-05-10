from __future__ import annotations

from typing import Any, Dict

from product.app_binding.runtime.persistence import persist_session
from product.core.runtime.flow_orchestrator import run_full_flow


def execute_bound_flow(
    ctx: Dict[str, Any],
    user_a: Dict[str, Any],
    user_b: Dict[str, Any],
) -> Dict[str, Any]:
    """Run MATCH → UNLOCK → INSIGHT and persist session for UI reload."""
    _ = ctx  # reserved for auth / session context in later UI integration
    full = run_full_flow(user_a, user_b)
    insight_state = full["unlock"]["insight"]
    payload = {
        "flow_result": full,
        "insight_state": insight_state,
    }
    persist_session(payload)
    return {
        **full,
        "insight_state": insight_state,
        "flow_result": full,
    }
