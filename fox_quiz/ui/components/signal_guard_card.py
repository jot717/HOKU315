from __future__ import annotations

from typing import Any, Union

import reflex as rx

from fox_quiz.ui.components.warning_signal_chip import warning_signal_chip


def _risk_flag_row(
    risk_level: Union[str, rx.Var[str]],
    risk_flags: Any,
) -> rx.Component:
    if isinstance(risk_flags, (list, tuple)):
        items = [str(x) for x in risk_flags if str(x).strip()][:12]
        if not items:
            return rx.fragment()
        return rx.hstack(
            *[warning_signal_chip(item, risk_level) for item in items],
            spacing="2",
            width="100%",
            flex_wrap="wrap",
        )
    return rx.text(
        "（訊號旗標由狀態載入）",
        size="2",
        color="gray",
        as_="span",
    )


def signal_guard_card(
    risk_level: Union[str, rx.Var[str]],
    risk_flags: Any,
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
                _risk_flag_row(risk_level, risk_flags),
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
