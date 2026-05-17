from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

import pytest

from product.persistence.runtime import registry
from product.persistence.runtime.backend import LocalJsonBackend
from product.persistence.runtime.entities import ENTITY_PATHS

ROOT = Path(__file__).resolve().parents[2]
REPO_RUNTIME = ROOT / "runtime_state"

RUNTIME_ARTIFACTS = tuple(p.name for p in ENTITY_PATHS.values())


def _unlink_repo_runtime_artifacts() -> None:
    for name in RUNTIME_ARTIFACTS:
        path = REPO_RUNTIME / name
        if path.is_file():
            path.unlink()


@pytest.fixture
def isolated_persistence(tmp_path: Path) -> dict[str, Path]:
    """Isolated LocalJsonBackend rooted in tmp_path (not repo runtime_state/)."""
    registry.reset_backend_for_tests()
    paths = {key: tmp_path / f"{key}.json" for key in ENTITY_PATHS}
    registry.use_backend(LocalJsonBackend(paths))
    yield paths
    registry.use_backend(None)
    registry.reset_backend_for_tests()


@pytest.fixture(autouse=True)
def _uat_runtime_hygiene() -> Iterator[None]:
    registry.use_backend(None)
    registry.reset_backend_for_tests()
    yield
    registry.use_backend(None)
    registry.reset_backend_for_tests()
    _unlink_repo_runtime_artifacts()


def read_disk_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)
