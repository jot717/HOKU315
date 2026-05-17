from __future__ import annotations

from typing import Any

SCHEMA_VERSION = 1


def with_schema_version(payload: dict[str, Any]) -> dict[str, Any]:
    out = dict(payload)
    out["schema_version"] = SCHEMA_VERSION
    return out


def read_schema_version(raw: Any, *, default: int = 1) -> int:
    if not isinstance(raw, dict):
        return default
    try:
        return int(raw.get("schema_version", default))
    except (TypeError, ValueError):
        return default
