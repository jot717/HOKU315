from __future__ import annotations

from typing import Union

import reflex as rx


def fox_memory_card(
    note: Union[str, rx.Var[str]],
    recurring: Union[str, rx.Var[str]],
) -> rx.Component:
    """Frosted guardian diary — remembers recent observation tone (local rules only)."""
    main_line = rx.cond(
        note != "",
        rx.text(
            note,
            size="3",
            style={"line_height": "1.75"},
            as_="span",
        ),
        rx.text(
            "多觀察幾次，北極狐就能替你收斂長一點的記憶。",
            size="3",
            color="gray",
            style={"line_height": "1.75"},
            as_="span",
        ),
    )
    return rx.box(
        rx.vstack(
            rx.text(
                "北極狐的守護筆記",
                size="2",
                weight="bold",
                color="gray",
                letter_spacing="0.04em",
                as_="span",
            ),
            main_line,
            rx.text(
                recurring,
                size="2",
                color="gray",
                style={"line_height": "1.65"},
                as_="span",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        padding="1.35rem 1.5rem",
        border_radius="18px",
        width="100%",
        border="1px solid rgba(255,255,255,0.92)",
        background="rgba(255,255,255,0.78)",
        style={
            "backdropFilter": "blur(10px)",
            "boxShadow": "0 10px 36px rgba(155, 185, 215, 0.14)",
        },
    )
