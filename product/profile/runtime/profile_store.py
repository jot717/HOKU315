from __future__ import annotations

from typing import Any, Dict

from product.persistence.runtime.entities import USER_PROFILE
from product.persistence.runtime.registry import get_backend

DEFAULT_PROFILE = {
    "name": "Demo User",
    "interests": ["ai", "music"],
    "activity": 5,
}


def save_profile(profile: Dict[str, Any]) -> None:
    get_backend().write(USER_PROFILE, profile)


def load_profile() -> Dict[str, Any]:
    data = get_backend().read(USER_PROFILE)
    if data is None:
        save_profile(DEFAULT_PROFILE)
        return dict(DEFAULT_PROFILE)
    return data
