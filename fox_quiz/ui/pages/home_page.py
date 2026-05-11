from __future__ import annotations

import reflex as rx

from fox_quiz.ui.components.world_container import world_container


def home_page() -> rx.Component:
    return world_container(
        rx.container(
            rx.vstack(
                rx.heading(
                    "HOKU315",
                    size="9",
                ),
                rx.heading(
                    "進入北極狐的觀察世界",
                    size="6",
                    weight="medium",
                    text_align="center",
                ),
                rx.text(
                    "讓 AI 替你過濾消耗你的訊號",
                    size="4",
                    color="gray",
                    text_align="center",
                    style={"line_height": "1.6"},
                    max_width="26rem",
                    as_="span",
                ),
                rx.vstack(
                    rx.link(
                        rx.button(
                            "建立個人資料",
                            width="100%",
                            size="4",
                            variant="soft",
                        ),
                        href="/profile",
                        width="100%",
                    ),
                    rx.link(
                        rx.button(
                            "進入觀察室",
                            width="100%",
                            size="4",
                            color_scheme="orange",
                        ),
                        href="/insight",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                    max_width="22rem",
                ),
                spacing="9",
                align="center",
                width="100%",
                max_width="32rem",
            ),
            padding_y="4rem",
            padding_x="1.5rem",
            width="100%",
        ),
    )
