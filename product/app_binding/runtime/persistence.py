from __future__ import annotations

from typing import Any, Dict

from product.persistence.runtime.entities import LOCAL_SESSION
from product.persistence.runtime.registry import get_backend


def persist_session(data: Dict[str, Any]) -> None:
    get_backend().write(LOCAL_SESSION, data)


def load_session() -> Dict[str, Any]:
    raw = get_backend().read(LOCAL_SESSION)
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    return {}
