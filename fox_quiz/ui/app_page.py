from __future__ import annotations

import reflex as rx

from fox_quiz.ui.components.world_container import world_container
from fox_quiz.ui.insight_panel import insight_panel


def app_page() -> rx.Component:
    return world_container(
        rx.container(
            rx.vstack(
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "HOKU315",
                            size="8",
                            weight="bold",
                        ),
                        rx.text(
                            "極狐觀察室",
                            size="4",
                            color="gray",
                            as_="span",
                        ),
                        spacing="3",
                        align="center",
                        width="100%",
                    ),
                    width="100%",
                    padding_bottom="3",
                ),
                insight_panel(),
                spacing="8",
                width="100%",
                max_width="42rem",
                align="center",
            ),
            padding_y="3rem",
            padding_x="1.25rem",
            width="100%",
        ),
    )
