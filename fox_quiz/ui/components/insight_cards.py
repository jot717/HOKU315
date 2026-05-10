from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState


def insight_cards() -> rx.Component:
    """Single emphasis card for narrative insight (score + energy live in hero_insight)."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "深度洞察",
                size="4",
                weight="medium",
            ),
            rx.text(
                AppState.final_insight,
                size="3",
                style={"line_height": "1.7"},
                as_="span",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        padding="1.25em",
        width="100%",
        border_radius="16px",
        border="1px solid var(--gray-6)",
        background="var(--gray-1)",
    )
