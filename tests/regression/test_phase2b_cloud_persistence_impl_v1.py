from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

import db_service
from product.persistence.runtime import registry
from product.persistence.runtime.dual_write_backend import DualWriteBackend
from product.persistence.runtime.entities import USER_PROFILE
from product.persistence.runtime.sync_context import set_access_token_provider
from product.persistence.runtime.sync_status import get_entity_status, load_sync_status
from product.profile.runtime.profile_store import load_profile, save_profile

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def dual_cloud_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    registry.reset_backend_for_tests()
    set_access_token_provider(None)
    monkeypatch.setenv("HOKU_PERSISTENCE_BACKEND", "dual")
    monkeypatch.setenv("HOKU_CLOUD_SYNC_ENABLED", "1")
    monkeypatch.setenv("HOKU_CLOUD_PERSISTENCE_MOCK", "1")
    monkeypatch.setenv("MOCK_LOGIN_USER_ID", "uat-user-001")
    monkeypatch.setenv("HOKU_ACCESS_TOKEN", "mock-jwt")
    monkeypatch.setattr(db_service, "_MOCK_CLOUD_ROOT", tmp_path / "cloud_mock")
    yield
    registry.reset_backend_for_tests()
    set_access_token_provider(None)


def test_dual_write_local_first_then_cloud(dual_cloud_env: None, tmp_path: Path) -> None:
    registry.reset_backend_for_tests()
    paths = {k: tmp_path / f"{k}.json" for k in ("user_profile", "target_profile", "fox_memory", "session_history", "local_session")}
    from product.persistence.runtime.entities import ENTITY_PATHS

    paths = {k: tmp_path / f"{k}.json" for k in ENTITY_PATHS}
    registry.use_backend(
        DualWriteBackend(
            local=__import__(
                "product.persistence.runtime.backend", fromlist=["LocalJsonBackend"]
            ).LocalJsonBackend(paths),
        )
    )

    save_profile({"name": "Cloud User", "interests": ["signal"], "activity": 6})
    assert load_profile()["name"] == "Cloud User"

    mock_file = tmp_path / "cloud_mock" / "uat-user-001" / "user_profile.json"
    assert mock_file.is_file()
    cloud_doc = json.loads(mock_file.read_text(encoding="utf-8"))
    assert cloud_doc["payload"]["name"] == "Cloud User"

    status = get_entity_status("user_profile")
    assert status.get("status") == "synced"


def test_cloud_failure_marks_pending_not_destroying_local(
    dual_cloud_env: None, tmp_path: Path,
) -> None:
    from product.persistence.runtime.backend import LocalJsonBackend
    from product.persistence.runtime.entities import ENTITY_PATHS

    paths = {k: tmp_path / f"{k}.json" for k in ENTITY_PATHS}
    registry.use_backend(DualWriteBackend(local=LocalJsonBackend(paths)))

    save_profile({"name": "Stable Local", "interests": [], "activity": 5})
    before = paths[USER_PROFILE].read_text(encoding="utf-8")

    with patch.object(db_service, "persistence_upsert_entity", side_effect=RuntimeError("offline")):
        save_profile({"name": "After Fail", "interests": [], "activity": 5})

    assert paths[USER_PROFILE].read_text(encoding="utf-8") == before.replace("Stable Local", "After Fail")
    assert get_entity_status("user_profile").get("status") == "pending"


def test_guest_mode_stays_local_only(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    registry.reset_backend_for_tests()
    set_access_token_provider(None)
    monkeypatch.setenv("HOKU_PERSISTENCE_BACKEND", "dual")
    monkeypatch.setenv("HOKU_CLOUD_SYNC_ENABLED", "1")
    monkeypatch.setenv("HOKU_CLOUD_PERSISTENCE_MOCK", "1")
    monkeypatch.delenv("MOCK_LOGIN_USER_ID", raising=False)
    monkeypatch.delenv("HOKU_ACCESS_TOKEN", raising=False)

    from product.persistence.runtime.backend import LocalJsonBackend
    from product.persistence.runtime.entities import ENTITY_PATHS

    paths = {k: tmp_path / f"{k}.json" for k in ENTITY_PATHS}
    registry.use_backend(DualWriteBackend(local=LocalJsonBackend(paths)))

    save_profile({"name": "Guest Only", "interests": [], "activity": 3})
    assert load_profile()["name"] == "Guest Only"
    assert not (tmp_path / "cloud_mock").exists()


def test_cloud_backend_has_no_supabase_import() -> None:
    text = (ROOT / "product/persistence/runtime/cloud_backend.py").read_text(encoding="utf-8")
    assert "create_client" not in text
    assert "db_service" in text


def test_lww_cloud_newer_wins_on_read(dual_cloud_env: None, tmp_path: Path) -> None:
    from datetime import datetime, timezone

    from product.persistence.runtime.backend import LocalJsonBackend
    from product.persistence.runtime.entities import ENTITY_PATHS

    paths = {k: tmp_path / f"{k}.json" for k in ENTITY_PATHS}
    registry.use_backend(DualWriteBackend(local=LocalJsonBackend(paths)))

    save_profile({"name": "Local Older", "interests": [], "activity": 1})
    cloud_path = tmp_path / "cloud_mock" / "uat-user-001" / "user_profile.json"
    cloud_path.parent.mkdir(parents=True, exist_ok=True)
    newer = datetime(2099, 1, 1, tzinfo=timezone.utc).isoformat()
    cloud_path.write_text(
        json.dumps(
            {
                "updated_at": newer,
                "payload": {"name": "Cloud Newer", "interests": ["x"], "activity": 9},
                "schema_version": 1,
            }
        ),
        encoding="utf-8",
    )

    loaded = load_profile()
    assert loaded["name"] == "Cloud Newer"
    assert json.loads(paths[USER_PROFILE].read_text(encoding="utf-8"))["name"] == "Cloud Newer"


def test_registry_dual_without_flag_stays_local(monkeypatch: pytest.MonkeyPatch) -> None:
    registry.reset_backend_for_tests()
    monkeypatch.setenv("HOKU_PERSISTENCE_BACKEND", "dual")
    monkeypatch.setenv("HOKU_CLOUD_SYNC_ENABLED", "0")
    from product.persistence.runtime.backend import LocalJsonBackend

    backend = registry.get_backend()
    assert isinstance(backend, LocalJsonBackend)
