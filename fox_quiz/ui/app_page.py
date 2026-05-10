from __future__ import annotations

import reflex as rx

from fox_quiz.ui.insight_panel import insight_panel
from fox_quiz.ui.profile.profile_editor import profile_editor


def app_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading(
                "HOKU315",
                size="8",
            ),
            profile_editor(),
            insight_panel(),
            spacing="6",
            width="100%",
        ),
        padding="2em",
    )
