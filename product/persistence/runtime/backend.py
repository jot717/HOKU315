from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Protocol

from product.persistence.runtime.entities import ENTITY_PATHS


class PersistenceBackend(Protocol):
    """Read/write JSON entities by canonical key."""

    def read(self, entity: str) -> Any | None:
        ...

    def write(self, entity: str, data: Any) -> None:
        ...


class LocalJsonBackend:
    """Default Phase 1/2-A backend: one JSON file per entity under runtime_state/."""

    def __init__(self, paths: dict[str, Path] | None = None) -> None:
        self._paths = paths or dict(ENTITY_PATHS)

    def path_for(self, entity: str) -> Path:
        if entity not in self._paths:
            raise KeyError(f"unknown persistence entity: {entity}")
        return self._paths[entity]

    def read(self, entity: str) -> Any | None:
        path = self.path_for(entity)
        if not path.exists():
            return None
        with path.open(encoding="utf-8") as f:
            return json.load(f)

    def write(self, entity: str, data: Any) -> None:
        path = self.path_for(entity)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
