"""PHASE2-B cloud persistence UAT — mock cloud store only."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

import db_service
from product.app_binding.runtime.persistence import load_session, persist_session
from product.persistence.runtime import registry
from product.persistence.runtime.dual_write_backend import DualWriteBackend
from product.persistence.runtime.entities import ENTITY_PATHS, LOCAL_SESSION, USER_PROFILE
from product.persistence.runtime.sync_status import get_entity_status
from product.profile.runtime.profile_store import load_profile, save_profile

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def cloud_dual(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    registry.reset_backend_for_tests()
    monkeypatch.setenv("HOKU_PERSISTENCE_BACKEND", "dual")
    monkeypatch.setenv("HOKU_CLOUD_SYNC_ENABLED", "1")
    monkeypatch.setenv("HOKU_CLOUD_PERSISTENCE_MOCK", "1")
    monkeypatch.setenv("MOCK_LOGIN_USER_ID", "uat-cloud-1")
    monkeypatch.setenv("HOKU_ACCESS_TOKEN", "token-1")
    monkeypatch.setattr(db_service, "_MOCK_CLOUD_ROOT", tmp_path / "cloud_mock")
    paths = {k: tmp_path / f"{k}.json" for k in ENTITY_PATHS}
    from product.persistence.runtime.backend import LocalJsonBackend

    registry.use_backend(DualWriteBackend(local=LocalJsonBackend(paths)))
    yield paths
    registry.reset_backend_for_tests()


def test_uat_local_session_never_cloud_synced(cloud_dual: dict[str, Path]) -> None:
    persist_session({"flow_step": "insight"})
    assert load_session().get("flow_step") == "insight"
    mock_root = db_service._MOCK_CLOUD_ROOT
    assert not list(mock_root.glob("**/local_session.json"))


def test_uat_dual_write_profile_cloud_mirror(cloud_dual: dict[str, Path]) -> None:
    save_profile({"name": "UAT Cloud", "interests": ["a"], "activity": 4})
    assert load_profile()["name"] == "UAT Cloud"
    mock_file = db_service._MOCK_CLOUD_ROOT / "uat-cloud-1" / "user_profile.json"
    assert mock_file.is_file()
    assert get_entity_status("user_profile").get("status") == "synced"


def test_uat_offline_flag_defaults_local_only(monkeypatch: pytest.MonkeyPatch) -> None:
    registry.reset_backend_for_tests()
    monkeypatch.setenv("HOKU_PERSISTENCE_BACKEND", "local")
    monkeypatch.delenv("HOKU_CLOUD_SYNC_ENABLED", raising=False)
    from product.persistence.runtime.backend import LocalJsonBackend

    assert isinstance(registry.get_backend(), LocalJsonBackend)
