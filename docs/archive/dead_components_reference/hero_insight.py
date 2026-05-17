from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState


def hero_insight() -> rx.Component:
    """Large signal-safety hero: score, guardian headline, supporting line."""
    return rx.box(
        rx.vstack(
            rx.text(
                "訊號守護指數",
                size="2",
                weight="medium",
                color="gray",
                letter_spacing="0.06em",
                as_="span",
            ),
            rx.heading(
                AppState.match_score_heading,
                size="9",
                weight="bold",
                style={"line_height": "1.05"},
            ),
            rx.progress(
                value=AppState.match_score_safe_int,
                max=100,
                width="100%",
                size="3",
                color_scheme="orange",
            ),
            rx.divider(size="4", margin_y="2"),
            rx.heading(
                AppState.compatibility_title,
                size="6",
                weight="medium",
                text_align="center",
                style={"line_height": "1.35"},
            ),
            rx.text(
                AppState.energy_summary,
                size="4",
                color="gray",
                text_align="center",
                style={"line_height": "1.6"},
                as_="span",
            ),
            rx.text(
                "這份觀察幫你看見距離與界線，讓你決定要不要靠近。",
                size="2",
                opacity=0.75,
                text_align="center",
                as_="span",
            ),
            spacing="5",
            align="center",
            width="100%",
        ),
        padding_y="2.5rem",
        padding_x="1.75rem",
        border_radius="16px",
        width="100%",
        background="rgba(255,255,255,0.88)",
        border="1px solid rgba(255,255,255,0.95)",
        style={"boxShadow": "0 12px 40px rgba(150, 178, 210, 0.12)"},
    )
