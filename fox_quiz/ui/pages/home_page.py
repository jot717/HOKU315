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
                    "這裡是：社交互動保護系統。用守護視角替你過濾危險訊號與「互動環境」——你在觀察的是危險互動模式，不是在做性格測驗。",
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
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "你接下來會經歷的事",
                            size="4",
                            weight="medium",
                            text_align="center",
                        ),
                        rx.text(
                            "① 建立訊號檔案（/profile）\n"
                            "② 設定觀察對象（/target）：描述互動節奏，不是交友檔案\n"
                            "③ 進入觀察室（/insight）：北極狐把你的訊號與對象訊號疊看壓力\n"
                            "④ 可選：20 題地雷滑桿（/quiz）加深敏感度畫像\n"
                            "⑤ 未來接上社群訊號與社交圖保護層",
                            size="2",
                            color="gray",
                            text_align="center",
                            style={
                                "line_height": "1.85",
                                "white_space": "pre-wrap",
                                "font_variant_numeric": "tabular-nums",
                            },
                            as_="span",
                        ),
                        rx.text(
                            "精簡路徑：訊號檔案 → 觀察對象 → 觀察室（需要更深時再到測驗頁）",
                            size="1",
                            color="gray",
                            text_align="center",
                            style={"line_height": "1.65"},
                            as_="span",
                        ),
                        spacing="3",
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
                            "設定觀察對象",
                            width="100%",
                            size="4",
                            variant="outline",
                        ),
                        href="/target",
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
