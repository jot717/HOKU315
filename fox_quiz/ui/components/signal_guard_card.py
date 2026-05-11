from __future__ import annotations

from typing import Union

import reflex as rx

from fox_quiz.ui.components.warning_signal_chip import warning_signal_chip


def signal_guard_card(
    risk_level: Union[str, rx.Var[str]],
    risk_flags: rx.Var[list[str]],
    guardian_warning: Union[str, rx.Var[str]],
) -> rx.Component:
    tone_title = rx.cond(
        risk_level == "high",
        "守護警示：先拉開距離",
        rx.cond(risk_level == "medium", "守護提醒：先觀察邊界", "守護狀態：目前平穩"),
    )
    return rx.box(
        rx.vstack(
            rx.text(
                "訊號守護機制",
                size="2",
                weight="bold",
                color="gray",
                as_="span",
            ),
            rx.heading(
                tone_title,
                size="4",
                weight="medium",
            ),
            rx.text(
                guardian_warning,
                size="3",
                color="gray",
                style={"line_height": "1.7"},
                as_="span",
            ),
            rx.hstack(
                rx.foreach(
                    risk_flags,
                    lambda flag: warning_signal_chip(flag, risk_level),
                ),
                spacing="2",
                width="100%",
                flex_wrap="wrap",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        padding="1.35rem 1.5rem",
        border_radius="18px",
        width="100%",
        border="1px solid rgba(255,255,255,0.92)",
        background="rgba(255,255,255,0.8)",
        style={
            "backdropFilter": "blur(10px)",
            "boxShadow": "0 10px 36px rgba(155, 185, 215, 0.14)",
        },
    )
