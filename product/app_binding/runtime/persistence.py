from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

SESSION_FILE = Path(
    "runtime_state/local_session.json",
)


def persist_session(
    data: Dict[str, Any],
) -> None:
    SESSION_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        SESSION_FILE,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
        )


def load_session() -> Dict[str, Any]:
    if not SESSION_FILE.exists():
        return {}

    with open(
        SESSION_FILE,
        encoding="utf-8",
    ) as f:
        return json.load(f)
