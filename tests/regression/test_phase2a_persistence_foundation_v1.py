from __future__ import annotations

import os
from pathlib import Path

import pytest

from product.persistence.runtime import registry
from product.persistence.runtime.backend import LocalJsonBackend
from product.persistence.runtime.entities import ENTITY_PATHS, USER_PROFILE
from product.profile.runtime.profile_store import DEFAULT_PROFILE, load_profile, save_profile

ROOT = Path(__file__).resolve().parents[2]


def test_persistence_package_exists() -> None:
    assert (ROOT / "product/persistence/runtime/backend.py").is_file()
    assert (ROOT / "product/persistence/runtime/registry.py").is_file()
    assert len(ENTITY_PATHS) >= 5


def test_default_backend_is_local() -> None:
    registry.reset_backend_for_tests()
    os.environ.pop("HOKU_PERSISTENCE_BACKEND", None)
    backend = registry.get_backend()
    assert isinstance(backend, LocalJsonBackend)


def test_unsupported_backend_raises() -> None:
    registry.reset_backend_for_tests()
    os.environ["HOKU_PERSISTENCE_BACKEND"] = "supabase"
    os.environ.pop("HOKU_CLOUD_SYNC_ENABLED", None)
    try:
        with pytest.raises(ValueError, match="unsupported"):
            registry.get_backend()
    finally:
        os.environ.pop("HOKU_PERSISTENCE_BACKEND", None)
        registry.reset_backend_for_tests()


def test_profile_roundtrip_via_backend(tmp_path) -> None:
    registry.reset_backend_for_tests()
    paths = {k: tmp_path / f"{k}.json" for k in ENTITY_PATHS}
    registry.use_backend(LocalJsonBackend(paths))

    payload = dict(DEFAULT_PROFILE)
    payload["name"] = "Phase2A Test"
    save_profile(payload)
    loaded = load_profile()
    assert loaded["name"] == "Phase2A Test"


def test_persistence_module_has_no_supabase_import() -> None:
    text = (ROOT / "product/persistence/runtime/registry.py").read_text(encoding="utf-8")
    assert "supabase" not in text.lower()
