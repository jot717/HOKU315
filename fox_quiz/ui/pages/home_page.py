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
                    "分析危險互動節奏、社交電量消耗與適合你的相處方式——"
                    "不是約會分數，也不是性格測驗。",
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
                            "1. 建立訊號檔案 → 2. 完成問卷 → 3. 設定觀察對象\n"
                            "4. 查看互動分析 → 5. 瀏覽社交電量相容對象",
                            size="3",
                            color="gray",
                            text_align="left",
                            style={
                                "line_height": "1.85",
                                "white_space": "pre-wrap",
                            },
                            width="100%",
                            as_="span",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    padding="1.25rem",
                    border_radius="16px",
                    width="100%",
                    max_width="28rem",
                    border="1px dashed rgba(160, 185, 215, 0.55)",
                    background="rgba(255,255,255,0.5)",
                ),
                rx.card(
                    rx.vstack(
                        rx.text("訪客模式", size="3", weight="bold", as_="span"),
                        rx.text(
                            "無需帳號即可在本機完成訊號分析；資料主要保存在此裝置，"
                            "換裝置可能需重新填寫。",
                            size="2",
                            color="gray",
                            as_="span",
                            style={"line_height": "1.6"},
                        ),
                        rx.link(
                            rx.button(
                                "立即開始分析",
                                width="100%",
                                size="4",
                                color_scheme="orange",
                            ),
                            href="/profile",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    width="100%",
                    max_width="28rem",
                ),
                rx.card(
                    rx.vstack(
                        rx.text("帳號模式", size="3", weight="bold", as_="span"),
                        rx.text(
                            "登入後可保存問卷向量、故事與配對牆資料，"
                            "並累積長期互動趨勢（跨裝置備份逐步完善）。",
                            size="2",
                            color="gray",
                            as_="span",
                            style={"line_height": "1.6"},
                        ),
                        rx.link(
                            rx.button(
                                "登入以保存長期互動趨勢",
                                width="100%",
                                size="4",
                                variant="outline",
                                color_scheme="orange",
                            ),
                            href="/login",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    width="100%",
                    max_width="28rem",
                ),
                rx.text(
                    "北極狐只在分析頁提供簡短觀察，協助你看懂節奏與壓力，"
                    "不是心理諮商或治療。",
                    size="2",
                    color="gray",
                    text_align="center",
                    style={"line_height": "1.7", "white_space": "pre-wrap"},
                    max_width="28rem",
                    as_="span",
                ),
                spacing="6",
                align="center",
                width="100%",
                max_width="32rem",
            ),
            padding_y="4rem",
            padding_x="1.5rem",
            width="100%",
        ),
    )
