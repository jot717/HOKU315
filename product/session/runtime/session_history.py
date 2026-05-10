from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

SESSION_HISTORY_PATH = Path(
    "runtime_state/session_history.json",
)

MAX_HISTORY = 20


def load_history() -> List[Dict[str, Any]]:
    if not SESSION_HISTORY_PATH.exists():
        return []

    with open(
        SESSION_HISTORY_PATH,
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def append_history(item: Dict[str, Any]) -> None:
    history = load_history()

    history.insert(0, item)

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
