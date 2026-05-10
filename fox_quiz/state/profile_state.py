from __future__ import annotations

import reflex as rx

from product.profile.runtime.profile_engine import build_profile
from product.profile.runtime.profile_persistence import (
    load_profile as load_profile_disk,
    save_profile,
)


class ProfileState(rx.State):
    interests_text: str = ""
    activity_level: int = 5

    @rx.var(cache=True)
    def parsed_interests(self) -> list[str]:
        return [
            x.strip()
            for x in self.interests_text.split(",")
            if x.strip()
        ]

    @staticmethod
    def _coerce_slider(value: list[float | int] | float | int) -> int:
        if isinstance(value, (list, tuple)):
            if not value:
                return 5
            return int(value[0])
        return int(value)

    @rx.event
    def set_interests_text(self, value: str) -> None:
        self.interests_text = value

    @rx.event
    def set_activity_level(self, value: list[float | int] | float | int) -> None:
        v = self._coerce_slider(value)
        if v < 1:
            v = 1
        elif v > 10:
            v = 10
        self.activity_level = v

    @rx.event
    def save_current_profile(self) -> None:
        interests = [
            x.strip()
            for x in self.interests_text.split(",")
            if x.strip()
        ]
        profile = build_profile(
            interests,
            self.activity_level,
        )

        save_profile(profile)

    @rx.event
    def load_current_profile(self) -> None:
        profile = load_profile_disk()

        self.interests_text = ", ".join(
            profile.get(
                "interests",
                [],
            )
        )

        self.activity_level = int(
            profile.get(
                "activity",
                5,
            )
        )
