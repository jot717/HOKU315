"""
PHASE2-A — local-first persistence UAT (automated).

Validates persistence port stability before PHASE2-B planning.
No UI, cloud backend, or new product flows.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from product.app_binding.runtime.persistence import load_session, persist_session
from product.persistence.runtime import registry
from product.persistence.runtime.backend import LocalJsonBackend
from product.persistence.runtime.entities import (
    ENTITY_PATHS,
    SESSION_HISTORY,
    TARGET_PROFILE,
    USER_PROFILE,
)
from product.persistence.runtime.registry import get_backend
from product.profile.runtime.profile_store import DEFAULT_PROFILE, load_profile, save_profile
from product.session.runtime.session_history import append_history, load_history
from product.target.runtime.target_profile_store import (
    DEFAULT_TARGET,
    load_target_profile,
    normalize_target_profile,
    save_target_profile,
)
from tests.uat.conftest import read_disk_json

ROOT = Path(__file__).resolve().parents[2]
REPO_RUNTIME = ROOT / "runtime_state"


# --- 1. Restart persistence survival ---


def test_uat_restart_persistence_survival(isolated_persistence: dict[str, Path]) -> None:
    """Simulate process restart: new backend instance, same on-disk JSON."""
    paths = isolated_persistence

    save_profile({**DEFAULT_PROFILE, "name": "Survives Restart"})
    save_target_profile({**DEFAULT_TARGET, "target_name": "Restart Target"})
    append_history({"final_insight": "row-1", "compatibility_title": "", "energy_summary": ""})
    persist_session({"flow_step": "insight", "version": 1})

    registry.use_backend(None)
    registry.reset_backend_for_tests()
    registry.use_backend(LocalJsonBackend(paths))

    assert load_profile()["name"] == "Survives Restart"
    assert load_target_profile()["target_name"] == "Restart Target"
    assert load_history()[0]["final_insight"] == "row-1"
    assert load_session()["flow_step"] == "insight"


# --- 2. Timeline integrity ---


def test_uat_session_history_timeline_integrity(isolated_persistence: dict[str, Path]) -> None:
    append_history({"final_insight": "oldest", "compatibility_title": "c1", "energy_summary": "e1"})
    append_history({"final_insight": "middle", "compatibility_title": "c2", "energy_summary": "e2"})
    append_history({"final_insight": "newest", "compatibility_title": "c3", "energy_summary": "e3"})

    history = load_history()
    assert [row["final_insight"] for row in history[:3]] == ["newest", "middle", "oldest"]
    assert all(set(row.keys()) >= {"final_insight", "compatibility_title", "energy_summary"} for row in history)

    for i in range(25):
        append_history({"final_insight": f"fill-{i}", "compatibility_title": "", "energy_summary": ""})
    assert len(load_history()) <= 20


# --- 3. Profile merge stability ---


def test_uat_target_profile_merge_stability(isolated_persistence: dict[str, Path]) -> None:
    partial = {"target_name": "Merged Name", "instability_level": 9}
    save_target_profile(partial)
    loaded = load_target_profile()

    assert loaded["target_name"] == "Merged Name"
    assert loaded["instability_level"] == 9
    assert loaded["response_consistency"] == DEFAULT_TARGET["response_consistency"]
    assert isinstance(loaded["observed_traits"], list)

    merged = normalize_target_profile({**loaded, "notes": "  padded note  "})
    assert merged["notes"] == "padded note"
    assert merged["target_name"] == "Merged Name"


def test_uat_user_profile_roundtrip_stable(isolated_persistence: dict[str, Path]) -> None:
    payload = {**DEFAULT_PROFILE, "name": "UAT User", "activity": 7}
    save_profile(payload)
    again = load_profile()
    assert again["name"] == "UAT User"
    assert again["activity"] == 7


# --- 4. Duplicate persistence detection ---


def test_uat_no_duplicate_entity_paths() -> None:
    path_values = list(ENTITY_PATHS.values())
    assert len(path_values) == len(set(path_values))


def test_uat_single_file_per_entity_on_rewrite(isolated_persistence: dict[str, Path]) -> None:
    paths = isolated_persistence
    save_profile({"name": "v1", "interests": [], "activity": 1})
    save_profile({"name": "v2", "interests": ["x"], "activity": 2})

    profile_path = paths[USER_PROFILE]
    assert profile_path.is_file()
    assert profile_path.name == "user_profile.json"
    assert read_disk_json(profile_path)["name"] == "v2"
    assert not profile_path.with_suffix(".json.bak").exists()
    assert len(list(profile_path.parent.glob("user_profile*.json"))) == 1


# --- 5. Runtime vs disk state sync ---


def test_uat_runtime_matches_disk_json(isolated_persistence: dict[str, Path]) -> None:
    paths = isolated_persistence
    backend = get_backend()

    save_profile({**DEFAULT_PROFILE, "name": "Disk Sync"})
    disk = read_disk_json(paths[USER_PROFILE])
    runtime = backend.read(USER_PROFILE)
    api = load_profile()

    assert disk == runtime == api
    assert disk["name"] == "Disk Sync"

    append_history({"final_insight": "sync-check", "compatibility_title": "", "energy_summary": ""})
    disk_hist = read_disk_json(paths[SESSION_HISTORY])
    assert disk_hist == backend.read(SESSION_HISTORY)
    assert disk_hist[0]["final_insight"] == "sync-check"


# --- 6. Fail-fast backend validation ---


def test_uat_unsupported_backend_fails_fast(
    isolated_persistence: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry.reset_backend_for_tests()
    monkeypatch.delenv("HOKU_PERSISTENCE_BACKEND", raising=False)
    monkeypatch.setenv("HOKU_PERSISTENCE_BACKEND", "supabase")
    with pytest.raises(ValueError, match="unsupported"):
        get_backend()


def test_uat_unknown_entity_raises(isolated_persistence: dict[str, Path]) -> None:
    backend = get_backend()
    with pytest.raises(KeyError, match="unknown persistence entity"):
        backend.read("not_a_real_entity")


# --- 7. Deterministic cleanup behavior ---


def test_uat_repo_runtime_artifacts_absent_after_test(isolated_persistence: dict[str, Path]) -> None:
    """conftest autouse must not leave repo runtime_state JSON behind."""
    for name in ("user_profile.json", "target_profile.json", "session_history.json"):
        path = REPO_RUNTIME / name
        if path.is_file():
            path.unlink()

    save_profile({**DEFAULT_PROFILE, "name": "Should Not Leak"})
    assert isolated_persistence[USER_PROFILE].is_file()
    assert not (REPO_RUNTIME / "user_profile.json").exists()


# --- 8. Runtime state isolation between tests ---


def test_uat_isolation_side_a(isolated_persistence: dict[str, Path]) -> None:
    save_profile({**DEFAULT_PROFILE, "name": "Side-A-Only"})
    assert read_disk_json(isolated_persistence[USER_PROFILE])["name"] == "Side-A-Only"


def test_uat_isolation_side_b(isolated_persistence: dict[str, Path]) -> None:
    """Separate tmp_path; must not see Side-A-Only."""
    loaded = load_profile()
    assert loaded["name"] != "Side-A-Only"
    assert isolated_persistence[USER_PROFILE].parent != REPO_RUNTIME
