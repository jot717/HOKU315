from __future__ import annotations

from product.profile.runtime.profile_engine import build_profile


def test_profile_build() -> None:
    profile = build_profile(
        ["music", "ai"],
        7,
    )

    assert profile["activity"] == 7

    assert "music" in profile["interests"]
