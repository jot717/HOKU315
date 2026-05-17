from __future__ import annotations

import product.profile.runtime.profile_store as profile_store
from product.persistence.runtime import registry
from product.persistence.runtime.backend import LocalJsonBackend
from product.persistence.runtime.entities import USER_PROFILE


def test_profile_save_and_load(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        registry,
        "get_backend",
        lambda: LocalJsonBackend({USER_PROFILE: tmp_path / "user_profile.json"}),
    )

    profile = {
        "name": "Test",
        "interests": ["ai"],
        "activity": 3,
    }

    profile_store.save_profile(profile)

    loaded = profile_store.load_profile()

    assert loaded["name"] == "Test"
    assert loaded["activity"] == 3
