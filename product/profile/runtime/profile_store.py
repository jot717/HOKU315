from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

PROFILE_PATH = Path("runtime_state/user_profile.json")

DEFAULT_PROFILE = {
    "name": "Demo User",
    "interests": ["ai", "music"],
    "activity": 5,
}


def save_profile(profile: Dict[str, Any]) -> None:
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)


def load_profile() -> Dict[str, Any]:
    if not PROFILE_PATH.exists():
        save_profile(DEFAULT_PROFILE)

    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
