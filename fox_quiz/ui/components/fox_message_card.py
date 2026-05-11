from __future__ import annotations

from typing import Union

import reflex as rx


def fox_message_card(message: Union[str, rx.Var[str]]) -> rx.Component:
    return rx.cond(
        message != "",
        rx.box(
            rx.vstack(
                rx.text(
                    "北極狐觀察",
                    size="2",
                    weight="bold",
                    color="gray",
                ),
                rx.text(
                    message,
                    size="3",
                    style={"white_space": "pre-wrap", "line_height": "1.8"},
                    as_="span",
                ),
                spacing="3",
                align_items="start",
                width="100%",
            ),
            padding="1.25rem",
            border_radius="18px",
            background="white",
            border="1px solid var(--gray-4)",
            width="100%",
        ),
        rx.fragment(),
    )
