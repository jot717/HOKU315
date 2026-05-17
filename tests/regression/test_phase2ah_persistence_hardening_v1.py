from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from product.persistence.runtime import registry
from product.persistence.runtime.backend import LocalJsonBackend
from product.persistence.runtime.entities import ENTITY_PATHS, SESSION_HISTORY, USER_PROFILE
from product.persistence.runtime.schema import SCHEMA_VERSION
from product.profile.runtime.profile_store import load_profile, normalize_profile, save_profile
from product.session.runtime.session_history import append_history, load_history
from product.target.runtime.target_profile_store import load_target_profile, save_target_profile

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def isolated_backend(tmp_path: Path) -> dict[str, Path]:
    registry.reset_backend_for_tests()
    paths = {k: tmp_path / f"{k}.json" for k in ENTITY_PATHS}
    registry.use_backend(LocalJsonBackend(paths))
    yield paths
    registry.use_backend(None)
    registry.reset_backend_for_tests()


def test_profile_normalize_rejects_malformed_partial(isolated_backend: dict[str, Path]) -> None:
    dirty = {"name": 123, "interests": "a, b", "activity": "7", "evil": True}
    clean = normalize_profile(dirty)
    assert clean["name"] == "123"
    assert clean["interests"] == ["a", "b"]
    assert clean["activity"] == 7
    assert "evil" not in clean
    assert clean["schema_version"] == SCHEMA_VERSION


def test_profile_load_heals_corrupt_json(isolated_backend: dict[str, Path]) -> None:
    path = isolated_backend[USER_PROFILE]
    path.write_text("{not-json", encoding="utf-8")
    loaded = load_profile()
    assert loaded["schema_version"] == SCHEMA_VERSION
    assert path.read_text(encoding="utf-8").startswith("{")


def test_schema_version_written_on_save(isolated_backend: dict[str, Path]) -> None:
    save_profile({"name": "Versioned", "interests": ["x"], "activity": 4})
    on_disk = json.loads(isolated_backend[USER_PROFILE].read_text(encoding="utf-8"))
    assert on_disk["schema_version"] == SCHEMA_VERSION


def test_session_history_legacy_list_still_loads(isolated_backend: dict[str, Path]) -> None:
    path = isolated_backend[SESSION_HISTORY]
    path.write_text(
        json.dumps([{"final_insight": "legacy", "compatibility_title": "", "energy_summary": ""}]),
        encoding="utf-8",
    )
    rows = load_history()
    assert rows[0]["final_insight"] == "legacy"
    append_history({"final_insight": "new", "compatibility_title": "", "energy_summary": ""})
    packed = json.loads(path.read_text(encoding="utf-8"))
    assert packed["schema_version"] == SCHEMA_VERSION
    assert packed["items"][0]["final_insight"] == "new"


def test_atomic_write_preserves_file_on_failure(isolated_backend: dict[str, Path]) -> None:
    save_profile({"name": "Stable", "interests": [], "activity": 5})
    path = isolated_backend[USER_PROFILE]
    before = path.read_text(encoding="utf-8")
    assert not path.with_suffix(".json.tmp").exists()

    with patch(
        "product.persistence.runtime.backend.json.dump",
        side_effect=OSError("simulated write failure"),
    ):
        with pytest.raises(OSError, match="simulated"):
            save_profile({"name": "Broken", "interests": [], "activity": 1})

    assert path.read_text(encoding="utf-8") == before
    assert not path.with_suffix(".json.tmp").exists()


def test_target_partial_save_stays_normalized(isolated_backend: dict[str, Path]) -> None:
    save_target_profile({"target_name": "A", "instability_level": 11})
    loaded = load_target_profile()
    assert loaded["target_name"] == "A"
    assert loaded["instability_level"] == 10
    assert loaded["schema_version"] == SCHEMA_VERSION


def test_sanity_check_fix_routes_through_stores(isolated_backend: dict[str, Path], tmp_path: Path) -> None:
    """Fix path must not call json.dump directly in ops script."""
    text = (ROOT / "ops" / "env" / "runtime_sanity_check.py").read_text(encoding="utf-8")
    assert "json.dump(" not in text
    assert "reset_session_history" in text
    assert "persist_session" in text
