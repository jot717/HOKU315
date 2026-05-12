from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

SESSION_HISTORY_PATH = Path(
    "runtime_state/session_history.json",
)

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
    if not SESSION_HISTORY_PATH.exists():
        return []

    with open(
        SESSION_HISTORY_PATH,
        "r",
        encoding="utf-8",
    ) as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        return []
    return [_sanitize_row(x) for x in raw[:MAX_HISTORY]]


def append_history(item: Dict[str, Any]) -> None:
    history = load_history()

    history.insert(0, _sanitize_row(item))

    history = history[:MAX_HISTORY]

    SESSION_HISTORY_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        SESSION_HISTORY_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(history, f, indent=2)
