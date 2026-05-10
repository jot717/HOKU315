from __future__ import annotations

import reflex as rx

from fox_quiz.ui.insight_panel import insight_panel


def app_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading(
                "HOKU315",
                size="8",
            ),
            insight_panel(),
            spacing="6",
            width="100%",
        ),
        padding="2em",
    )
