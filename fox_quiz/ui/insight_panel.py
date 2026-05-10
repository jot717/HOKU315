from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState
from fox_quiz.ui.components.insight_cards import insight_cards


def insight_panel() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "AI Compatibility Insight",
            size="6",
        ),
        rx.button(
            "Run Match",
            on_click=AppState.run_demo_match,
        ),
        rx.button(
            "Load Last Session",
            on_click=AppState.load_latest_session,
        ),
        rx.cond(
            AppState.has_insight,
            rx.box(
                rx.text(
                    "Summary:",
                    weight="bold",
                ),
                rx.text(AppState.insight_ai_summary),
                rx.text(
                    "Shared Traits:",
                    weight="bold",
                ),
                rx.text(AppState.insight_shared_traits_text),
                rx.text(
                    "Activity Analysis:",
                    weight="bold",
                ),
                rx.text(AppState.insight_activity_analysis),
                insight_cards(),
                padding="1.5em",
                border="1px solid #333",
                border_radius="12px",
                width="100%",
            ),
            rx.text("No insight yet."),
        ),
        spacing="4",
        width="100%",
    )
