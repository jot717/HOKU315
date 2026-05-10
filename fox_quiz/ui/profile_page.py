from __future__ import annotations

import reflex as rx

from fox_quiz.state.profile_state import ProfileState


def profile_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Profile", size="6"),
            rx.input(
                value=ProfileState.name,
                on_change=ProfileState.set_name,
                placeholder="Name",
                width="100%",
            ),
            rx.input(
                value=ProfileState.interests_text,
                on_change=ProfileState.set_interests_text,
                placeholder="ai,music,travel",
                width="100%",
            ),
            rx.input(
                value=ProfileState.activity_text,
                on_change=ProfileState.set_activity_text,
                placeholder="Activity",
                width="100%",
            ),
            rx.button(
                "Save Profile",
                on_click=ProfileState.save_profile,
            ),
            rx.text(ProfileState.status_message),
            spacing="4",
            width="100%",
        ),
        padding="2em",
    )
