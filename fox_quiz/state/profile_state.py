from __future__ import annotations

import reflex as rx

from product.profile.runtime.profile_store import save_profile as persist_profile_to_disk
from product.profile.runtime.profile_store import load_profile as load_profile_from_store

PROFILE_SAVE_SUCCESS_MESSAGE = "你現在可以進入觀察室了。"


class ProfileState(rx.State):
    name: str = ""
    interests_text: str = ""
    activity_text: str = "5"
    status_message: str = ""

    @rx.event
    def sync_from_disk(self) -> None:
        p = load_profile_from_store()
        self.status_message = ""
        self.name = str(p.get("name", ""))
        interests = p.get("interests", [])
        if isinstance(interests, list):
            self.interests_text = ",".join(str(x) for x in interests)
        else:
            self.interests_text = ""
        self.activity_text = str(p.get("activity", 5))

    @rx.event
    def set_name(self, value: str) -> None:
        self.name = "" if value is None else str(value)

    @rx.event
    def set_interests_text(self, value: str) -> None:
        self.interests_text = "" if value is None else str(value)

    @rx.event
    def set_activity_text(self, value: str) -> None:
        self.activity_text = "" if value is None else str(value)

    @rx.event
    def save_profile(self) -> None:
        interests = [
            x.strip()
            for x in self.interests_text.split(",")
            if x.strip()
        ]

        try:
            raw_act = int(str(self.activity_text or "5").strip())
        except ValueError:
            raw_act = 5
        activity = max(1, min(10, raw_act))

        profile = {
            "name": self.name,
            "interests": interests,
            "activity": activity,
        }

        persist_profile_to_disk(profile)
        self.activity_text = str(activity)

        self.status_message = PROFILE_SAVE_SUCCESS_MESSAGE
