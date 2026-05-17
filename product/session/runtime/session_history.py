from __future__ import annotations

from typing import Any, Dict, List

from product.persistence.runtime.entities import SESSION_HISTORY
from product.persistence.runtime.registry import get_backend

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


def load_history() -> List[Dict[str, Any]]:
    raw = get_backend().read(SESSION_HISTORY)
    if raw is None:
        return []
    if not isinstance(raw, list):
        return []
    return [_sanitize_row(x) for x in raw[:MAX_HISTORY]]


def append_history(item: Dict[str, Any]) -> None:
    history = load_history()
    history.insert(0, _sanitize_row(item))
    history = history[:MAX_HISTORY]
    get_backend().write(SESSION_HISTORY, history)
