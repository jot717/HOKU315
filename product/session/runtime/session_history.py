from __future__ import annotations

from typing import Any, Dict, List

from product.persistence.runtime.entities import SESSION_HISTORY
from product.persistence.runtime.registry import get_backend
from product.persistence.runtime.schema import SCHEMA_VERSION, read_schema_version

MAX_HISTORY = 20


def _sanitize_row(row: Any) -> Dict[str, str]:
    """JSON/socket-safe row: only string fields used by the UI."""
    if not isinstance(row, dict):
        return {
            "compatibility_title": "",
            "energy_summary": "",
            "final_insight": "",
        }
    return {
        "compatibility_title": str(row.get("compatibility_title", "") or ""),
        "energy_summary": str(row.get("energy_summary", "") or ""),
        "final_insight": str(row.get("final_insight", "") or ""),
    }


def _pack_history(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "items": items[:MAX_HISTORY],
    }


def _unpack_history(raw: Any) -> List[Dict[str, Any]]:
    if isinstance(raw, list):
        rows = raw
    elif isinstance(raw, dict):
        read_schema_version(raw)
        items = raw.get("items", [])
        rows = items if isinstance(items, list) else []
    else:
        return []
    return [_sanitize_row(x) for x in rows[:MAX_HISTORY]]


def load_history() -> List[Dict[str, Any]]:
    raw = get_backend().read(SESSION_HISTORY)
    if raw is None:
        return []
    return _unpack_history(raw)


def append_history(item: Dict[str, Any]) -> None:
    history = load_history()
    history.insert(0, _sanitize_row(item))
    history = history[:MAX_HISTORY]
    get_backend().write(SESSION_HISTORY, _pack_history(history))


def reset_session_history() -> None:
    """Replace history with empty list (ops/sanity)."""
    get_backend().write(SESSION_HISTORY, _pack_history([]))
