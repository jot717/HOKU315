from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState


def _fox_card(
    *,
    accent: str,
    body: str,
    sub: str,
) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                "🦊",
                font_size="2.25rem",
                line_height="1",
                aria_hidden=True,
            ),
            rx.vstack(
                rx.text(
                    body,
                    size="4",
                    weight="medium",
                    as_="span",
                ),
                rx.text(
                    sub,
                    size="2",
                    color="gray",
                    as_="span",
                ),
                spacing="1",
                align_items="start",
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        padding="1.25rem 1.5rem",
        border_radius="20px",
        width="100%",
        background="rgba(255,255,255,0.92)",
        border="1px solid rgba(255,255,255,0.95)",
        style={
            "box_shadow": (
                f"0 0 0 1px rgba(255,255,255,0.6), "
                f"0 12px 40px {accent}, "
                "0 4px 16px rgba(160, 185, 220, 0.18)"
            ),
        },
    )


def fox_avatar() -> rx.Component:
    """Persistent fox presence — maps UI-only states from existing AppState."""
    return rx.cond(
        AppState.demo_match_loading,
        _fox_card(
            accent="rgba(120, 170, 255, 0.22)",
            body="我先替你檢查。",
            sub="北極狐正在觀察訊號",
        ),
        rx.cond(
            AppState.has_insight,
            rx.cond(
                AppState.match_score_safe_int < 45,
                _fox_card(
                    accent="rgba(255, 160, 120, 0.2)",
                    body="訊號需要慢下來。",
                    sub="先照顧自己的節奏，這也是守護。",
                ),
                _fox_card(
                    accent="rgba(140, 210, 190, 0.2)",
                    body="這裡很安全。",
                    sub="北極狐正在觀察訊號",
                ),
            ),
            _fox_card(
                accent="rgba(180, 200, 235, 0.25)",
                body="北極狐正在觀察訊號",
                sub="你不必獨自面對所有聲音。",
            ),
        ),
    )
