from __future__ import annotations

import reflex as rx


def home_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading(
                "HOKU315",
                size="9",
            ),
            rx.text(
                "情緒守護 · 訊號觀測",
                opacity=0.7,
                size="4",
            ),
            rx.text(
                "在雪白安靜的世界裡，\n北極狐會幫你避開消耗情緒的人與訊號。",
                size="3",
                color="gray",
                text_align="center",
                style={"line_height": "1.65"},
                max_width="420px",
                white_space="pre-wrap",
                as_="span",
            ),
            rx.text(
                "不是每個人都值得靠近。",
                size="2",
                color="gray",
                opacity=0.85,
                text_align="center",
                as_="span",
            ),
            rx.vstack(
                rx.link(
                    rx.button(
                        "建立個人資料",
                        width="100%",
                        size="4",
                    ),
                    href="/profile",
                    width="100%",
                ),
                rx.link(
                    rx.button(
                        "進入觀察室",
                        width="100%",
                        size="4",
                    ),
                    href="/insight",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            spacing="8",
            align="center",
            width="100%",
            max_width="500px",
        ),
        padding="4em",
    )
