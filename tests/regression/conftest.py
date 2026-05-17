from __future__ import annotations

from pathlib import Path

import pytest

from product.persistence.runtime import registry

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "runtime_state"

RUNTIME_ARTIFACTS = (
    "user_profile.json",
    "target_profile.json",
    "fox_memory.json",
    "session_history.json",
    "local_session.json",
)


def _clean_runtime_artifacts() -> None:
    for name in RUNTIME_ARTIFACTS:
        path = RUNTIME_DIR / name
        if path.is_file():
            path.unlink()


@pytest.fixture(autouse=True)
def _persistence_test_hygiene() -> None:
    registry.use_backend(None)
    registry.reset_backend_for_tests()
    yield
    registry.use_backend(None)
    registry.reset_backend_for_tests()
    _clean_runtime_artifacts()
