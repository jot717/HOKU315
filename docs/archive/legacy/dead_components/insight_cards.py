from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState


def insight_cards() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                "極狐寄語",
                size="4",
                weight="medium",
            ),
            rx.text(
                AppState.final_insight,
                size="3",
                style={"line_height": "1.75"},
                as_="span",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        padding="1.25em",
        width="100%",
        border_radius="18px",
        border="1px solid rgba(255,255,255,0.95)",
        background="rgba(255,255,255,0.85)",
        style={"boxShadow": "0 8px 28px rgba(155, 180, 210, 0.1)"},
    )
