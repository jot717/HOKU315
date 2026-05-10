from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState


def insight_cards() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.heading(
                "Compatibility",
                size="4",
            ),
            rx.text(
                AppState.compatibility_title,
                size="5",
            ),
            padding="1em",
            width="100%",
            border_radius="16px",
            border="1px solid #444",
        ),
        rx.box(
            rx.heading(
                "Shared Energy",
                size="4",
            ),
            rx.text(
                AppState.energy_summary,
            ),
            padding="1em",
            width="100%",
            border_radius="16px",
            border="1px solid #444",
        ),
        rx.box(
            rx.heading(
                "Final Insight",
                size="4",
            ),
            rx.text(
                AppState.final_insight,
            ),
            padding="1em",
            width="100%",
            border_radius="16px",
            border="1px solid #444",
        ),
        spacing="4",
        width="100%",
    )
