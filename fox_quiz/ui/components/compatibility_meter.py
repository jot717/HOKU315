from __future__ import annotations

from typing import Union

import reflex as rx


def compatibility_meter(
    score: Union[float, int, rx.Var],
    heading: Union[str, rx.Var],
) -> rx.Component:
    return rx.vstack(
        rx.heading(heading, size="5"),
        rx.progress(
            value=score,
            max=100,
            width="100%",
        ),
        spacing="2",
        width="100%",
    )
