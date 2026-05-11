from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState


def signal_scan_banner() -> rx.Component:
    """Immersive guardian scan strip — copy maps to load / idle / post-observe."""
    return rx.box(
        rx.cond(
            AppState.demo_match_loading,
            rx.hstack(
                rx.spinner(size="2"),
                rx.text(
                    "正在替你過濾危險訊號",
                    size="3",
                    weight="medium",
                    color="gray",
                    as_="span",
                ),
                spacing="3",
                align="center",
                width="100%",
                justify="center",
            ),
            rx.cond(
                AppState.has_insight,
                rx.hstack(
                    rx.text(
                        "情緒消耗風險已納入本次觀察",
                        size="3",
                        weight="medium",
                        color="gray",
                        as_="span",
                    ),
                    width="100%",
                    justify="center",
                ),
                rx.hstack(
                    rx.text(
                        "正在掃描互動壓力",
                        size="3",
                        weight="medium",
                        color="gray",
                        as_="span",
                    ),
                    width="100%",
                    justify="center",
                ),
            ),
        ),
        padding="1rem 1.25rem",
        border_radius="14px",
        width="100%",
        border="1px solid rgba(255,255,255,0.85)",
        background="rgba(255,255,255,0.5)",
        style={
            "backdropFilter": "blur(10px)",
            "boxShadow": "0 8px 32px rgba(140, 170, 210, 0.12)",
        },
    )
