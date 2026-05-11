from __future__ import annotations

import reflex as rx

from fox_quiz.ui.components.floating_snow import floating_snow


def world_container(*children: rx.Component) -> rx.Component:
    """Soft white dream-world shell: icy gradient, fog hint, centered content."""
    inner = rx.box(
        *children,
        position="relative",
        z_index="1",
        width="100%",
        min_height="100%",
    )
    return rx.box(
        floating_snow(),
        inner,
        position="relative",
        width="100%",
        min_height="100vh",
        overflow_x="hidden",
        style={
            "background": (
                "linear-gradient(165deg, "
                "#f8fbff 0%, #eef6ff 38%, #f4f9fc 72%, #eef4f8 100%)"
            ),
            "box_shadow": "inset 0 0 120px rgba(255,255,255,0.65)",
        },
    )
