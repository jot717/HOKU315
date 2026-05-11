from __future__ import annotations

from typing import Union

import reflex as rx


def warning_signal_chip(
    label: Union[str, rx.Var[str]],
    risk_level: Union[str, rx.Var[str]],
) -> rx.Component:
    return rx.badge(
        label,
        variant="surface",
        size="2",
        color_scheme=rx.cond(
            risk_level == "high",
            "amber",
            rx.cond(risk_level == "medium", "orange", "jade"),
        ),
    )
