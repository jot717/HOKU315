from __future__ import annotations

import reflex as rx

from fox_quiz.state.profile_state import ProfileState


def profile_editor() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Your Profile",
            size="5",
        ),
        rx.input(
            placeholder="music, ai, travel",
            value=ProfileState.interests_text,
            on_change=ProfileState.set_interests_text,
            width="100%",
        ),
        rx.text(
            "Activity Level",
        ),
        rx.slider(
            min=1,
            max=10,
            step=1,
            value=[ProfileState.activity_level],
            on_change=ProfileState.set_activity_level,
            width="100%",
        ),
        rx.button(
            "Save Profile",
            on_click=ProfileState.save_current_profile,
        ),
        rx.button(
            "Load Profile",
            on_click=ProfileState.load_current_profile,
        ),
        spacing="4",
        width="100%",
    )
