from __future__ import annotations

from typing import Any, Dict

from product.core.runtime.flow_orchestrator import run_full_flow
from product.profile.runtime.profile_store import load_profile

DEMO_TARGET = {
    "name": "Target User",
    "interests": ["music", "travel"],
    "activity": 7,
}


def run_profile_bound_flow() -> Dict[str, Any]:
    profile = load_profile()

    result = run_full_flow(profile, DEMO_TARGET)

    return {
        "profile": profile,
        "result": result,
    }
