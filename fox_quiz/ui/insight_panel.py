from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState
from fox_quiz.ui.components.compatibility_meter import compatibility_meter
from fox_quiz.ui.components.insight_cards import insight_cards
from fox_quiz.ui.components.session_history import session_history


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
        rx.button(
            "Refresh insight history",
            on_click=AppState.load_session_history,
        ),
        rx.cond(
            AppState.has_insight,
            rx.box(
                rx.vstack(
                    compatibility_meter(
                        AppState.match_score_safe_int,
                        AppState.match_score_heading,
                    ),
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
                    rx.cond(
                        AppState.show_final_card,
                        session_history(),
                    ),
                    spacing="3",
                    width="100%",
                ),
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
