from __future__ import annotations

from typing import Any, Dict


def build_profile(
    interests: list[str],
    activity: int,
) -> Dict[str, Any]:
    return {
        "interests": interests,
        "activity": activity,
    }
