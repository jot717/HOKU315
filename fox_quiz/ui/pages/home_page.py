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
                "AI 情緒匹配系統",
                opacity=0.7,
                size="4",
            ),
            rx.text(
                "先建立輪廓，再取得 AI 解析——每一步都為情緒洞察而設計。",
                size="2",
                color="gray",
                text_align="center",
                style={"line_height": "1.55"},
                max_width="420px",
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
                        "開始 AI 配對解析",
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
