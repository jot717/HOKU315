from __future__ import annotations

import reflex as rx

from fox_quiz.ui.components.world_container import world_container


def home_page() -> rx.Component:
    return world_container(
        rx.container(
            rx.vstack(
                rx.heading(
                    "AI 社交訊號分析系統",
                    size="8",
                    weight="bold",
                    text_align="center",
                ),
                rx.text(
                    "分析危險互動模式、情緒消耗風險與適合你的社交節奏。",
                    size="3",
                    color="gray",
                    text_align="center",
                    style={"line_height": "1.65"},
                    max_width="28rem",
                    as_="span",
                ),
                rx.box(
                    rx.vstack(
                        rx.text(
                            "1. 建立你的社交訊號檔案\n"
                            "2. 分析你的互動敏感度\n"
                            "3. 輸入你正在接觸的對象\n"
                            "4. 獲得危險互動分析結果\n"
                            "5. 查看適合你的社交類型",
                            size="3",
                            color="gray",
                            text_align="left",
                            style={
                                "line_height": "1.85",
                                "white_space": "pre-wrap",
                                "font_variant_numeric": "tabular-nums",
                            },
                            width="100%",
                            as_="span",
                        ),
                        spacing="2",
                        width="100%",
                        align="center",
                    ),
                    padding="1.25rem",
                    border_radius="16px",
                    width="100%",
                    max_width="28rem",
                    border="1px dashed rgba(160, 185, 215, 0.55)",
                    background="rgba(255,255,255,0.5)",
                ),
                rx.vstack(
                    rx.link(
                        rx.button(
                            "建立我的訊號檔案",
                            width="100%",
                            size="4",
                            variant="soft",
                        ),
                        href="/profile",
                        width="100%",
                    ),
                    rx.link(
                        rx.button(
                            "直接開始分析",
                            width="100%",
                            size="4",
                            color_scheme="orange",
                        ),
                        href="/quiz",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                    max_width="22rem",
                ),
                rx.text(
                    "北極狐會協助你理解分析結果，\n但真正的核心是社交訊號分析系統。",
                    size="2",
                    color="gray",
                    text_align="center",
                    style={"line_height": "1.7", "white_space": "pre-wrap"},
                    max_width="28rem",
                    as_="span",
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
