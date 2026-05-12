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
                    "北極狐守護世界",
                    size="6",
                    weight="medium",
                    text_align="center",
                ),
                rx.text(
                    "這裡不是交友軟體、不是性格測驗、也不是 AI 評分工具。",
                    size="3",
                    color="gray",
                    text_align="center",
                    style={"line_height": "1.65"},
                    max_width="28rem",
                    as_="span",
                ),
                rx.text(
                    "這裡是：用守護視角替你過濾危險訊號的世界。",
                    size="4",
                    weight="medium",
                    text_align="center",
                    style={"line_height": "1.55"},
                    max_width="28rem",
                    as_="span",
                ),
                rx.text(
                    "有些危險，\n不是在崩潰時出現。\n\n而是在你太累以前，\n就已經開始消耗你。",
                    size="3",
                    color="gray",
                    text_align="center",
                    style={"line_height": "1.7", "white_space": "pre-wrap"},
                    max_width="28rem",
                    as_="span",
                ),
                rx.vstack(
                    rx.link(
                        rx.button(
                            "建立訊號檔案",
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
