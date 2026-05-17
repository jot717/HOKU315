from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from product.persistence.runtime.entities import LOCAL_SESSION
from product.persistence.runtime.registry import get_backend
from product.persistence.runtime.schema import SCHEMA_VERSION, with_schema_version

_DEFAULT_SESSION: Dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
}


def normalize_local_session(raw: Dict[str, Any]) -> Dict[str, Any]:
    merged = deepcopy(_DEFAULT_SESSION)
    if isinstance(raw, dict):
        for key, value in raw.items():
            if key != "schema_version":
                merged[key] = value
    return with_schema_version(merged)


def persist_session(data: Dict[str, Any]) -> None:
    clean = normalize_local_session(data if isinstance(data, dict) else {})
    get_backend().write(LOCAL_SESSION, clean)


def load_session() -> Dict[str, Any]:
    raw = get_backend().read(LOCAL_SESSION)
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return normalize_local_session(raw)
    return {}
