from __future__ import annotations

import reflex as rx

from product.profile.runtime.profile_store import save_profile as persist_profile_to_disk
from product.profile.runtime.profile_store import load_profile as load_profile_from_store


class ProfileState(rx.State):
    name: str = ""
    interests_text: str = ""
    activity_text: str = "5"
    status_message: str = ""

    @rx.event
    def sync_from_disk(self) -> None:
        p = load_profile_from_store()
        self.name = str(p.get("name", ""))
        interests = p.get("interests", [])
        if isinstance(interests, list):
            self.interests_text = ",".join(str(x) for x in interests)
        else:
            self.interests_text = ""
        self.activity_text = str(p.get("activity", 5))

    @rx.event
    def set_name(self, value: str) -> None:
        self.name = value

    @rx.event
    def set_interests_text(self, value: str) -> None:
        self.interests_text = value

    @rx.event
    def set_activity_text(self, value: str) -> None:
        self.activity_text = value

    @rx.event
    def save_profile(self) -> None:
        interests = [
            x.strip()
            for x in self.interests_text.split(",")
            if x.strip()
        ]

        profile = {
            "name": self.name,
            "interests": interests,
            "activity": int(self.activity_text or "0"),
        }

        persist_profile_to_disk(profile)

        self.status_message = "Profile saved"
