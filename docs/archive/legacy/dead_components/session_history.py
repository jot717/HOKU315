from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState


def session_history() -> rx.Component:
    return rx.vstack(
        rx.heading("Past insights", size="4"),
        rx.foreach(
            AppState.session_history,
            lambda item: rx.box(
                rx.text(item["final_insight"]),
                padding="1em",
                border="1px solid #333",
                border_radius="12px",
                width="100%",
            ),
        ),
        width="100%",
    )
