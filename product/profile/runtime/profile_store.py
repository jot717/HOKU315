from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List

from product.persistence.runtime.entities import USER_PROFILE
from product.persistence.runtime.registry import get_backend
from product.persistence.runtime.schema import SCHEMA_VERSION, with_schema_version

DEFAULT_PROFILE: Dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "name": "Demo User",
    "interests": ["ai", "music"],
    "activity": 5,
}

_PROFILE_KEYS = frozenset({"name", "interests", "activity", "schema_version"})


def _coerce_interests(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [x.strip() for x in value.split(",") if x.strip()]
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    return []


def _coerce_activity(value: Any) -> int:
    try:
        n = int(round(float(value)))
    except (TypeError, ValueError):
        n = 5
    return max(0, min(10, n))


def normalize_profile(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic profile shape; unknown keys dropped."""
    merged = deepcopy(DEFAULT_PROFILE)
    if isinstance(raw, dict):
        merged.update({k: v for k, v in raw.items() if k in _PROFILE_KEYS})
    merged["name"] = str(merged.get("name", "")).strip()[:80] or "Demo User"
    merged["interests"] = _coerce_interests(merged.get("interests"))
    merged["activity"] = _coerce_activity(merged.get("activity"))
    return with_schema_version(merged)


def save_profile(profile: Dict[str, Any]) -> None:
    clean = normalize_profile(profile if isinstance(profile, dict) else {})
    get_backend().write(USER_PROFILE, clean)


def load_profile() -> Dict[str, Any]:
    raw = get_backend().read(USER_PROFILE)
    if raw is None or not isinstance(raw, dict):
        save_profile(dict(DEFAULT_PROFILE))
        return normalize_profile(dict(DEFAULT_PROFILE))
    return normalize_profile(raw)
