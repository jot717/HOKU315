from __future__ import annotations

import reflex as rx

from fox_quiz.state.target_state import TargetState
from fox_quiz.ui.components.world_container import world_container


def target_page() -> rx.Component:
    return world_container(
        rx.container(
            rx.vstack(
                rx.heading(
                    "設定觀察對象",
                    size="7",
                    weight="bold",
                    text_align="center",
                ),
                rx.text(
                    "輸入你正在互動、曖昧、交友或長期接觸的對象資料。",
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
                            "系統會分析：",
                            size="2",
                            weight="bold",
                            as_="span",
                        ),
                        rx.text(
                            "- 對方是否容易造成情緒消耗\n"
                            "- 是否存在操控模式\n"
                            "- 互動節奏是否失衡\n"
                            "- 長期關係風險",
                            size="2",
                            color="gray",
                            style={"line_height": "1.75", "white_space": "pre-wrap"},
                            as_="span",
                        ),
                        spacing="2",
                        align_items="start",
                        width="100%",
                    ),
                    padding="1rem",
                    border_radius="12px",
                    width="100%",
                    max_width="28rem",
                    border="1px solid rgba(200, 215, 235, 0.65)",
                    background="rgba(255,255,255,0.62)",
                ),
                rx.box(
                    rx.vstack(
                        rx.text("觀察對象怎麼稱呼", size="2", color="gray", as_="span"),
                        rx.input(
                            value=TargetState.target_name,
                            on_change=TargetState.set_target_name,
                            placeholder="例如：同事 A、線上聯絡人",
                            width="100%",
                        ),
                        rx.text("關係類型（粗略即可）", size="2", color="gray", as_="span"),
                        rx.input(
                            value=TargetState.relationship_type,
                            on_change=TargetState.set_relationship_type,
                            placeholder="例如：同事、朋友、合作方",
                            width="100%",
                        ),
                        rx.text(
                            "你觀察到的行為線索（逗號分隔）",
                            size="2",
                            color="gray",
                            as_="span",
                        ),
                        rx.input(
                            value=TargetState.observed_traits_text,
                            on_change=TargetState.set_observed_traits_text,
                            placeholder="常改期、訊息忽冷忽熱…",
                            width="100%",
                        ),
                        rx.text("溝通方式", size="2", color="gray", as_="span"),
                        rx.input(
                            value=TargetState.communication_style_text,
                            on_change=TargetState.set_communication_style_text,
                            placeholder="長語音、短句、已讀不回…",
                            width="100%",
                        ),
                        rx.text("社交節奏模式", size="2", color="gray", as_="span"),
                        rx.input(
                            value=TargetState.social_patterns_text,
                            on_change=TargetState.set_social_patterns_text,
                            placeholder="低潮才出現、聚會後消失…",
                            width="100%",
                        ),
                        rx.text("壓力訊號", size="2", color="gray", as_="span"),
                        rx.input(
                            value=TargetState.pressure_signals_text,
                            on_change=TargetState.set_pressure_signals_text,
                            placeholder="模糊承諾、比較、情緒重量…",
                            width="100%",
                        ),
                        rx.text("節奏不穩定度（0–10）", size="2", color="gray", as_="span"),
                        rx.hstack(
                            rx.slider(
                                min=0,
                                max=10,
                                step=1,
                                value=[TargetState.instability_level],
                                on_change=TargetState.set_instability_level,
                                width="100%",
                                flex="1",
                                color_scheme="orange",
                            ),
                            rx.badge(TargetState.instability_level, variant="soft"),
                            width="100%",
                            align="center",
                            spacing="3",
                        ),
                        rx.text("注意力需求（0–10）", size="2", color="gray", as_="span"),
                        rx.hstack(
                            rx.slider(
                                min=0,
                                max=10,
                                step=1,
                                value=[TargetState.attention_demand],
                                on_change=TargetState.set_attention_demand,
                                width="100%",
                                flex="1",
                                color_scheme="orange",
                            ),
                            rx.badge(TargetState.attention_demand, variant="soft"),
                            width="100%",
                            align="center",
                            spacing="3",
                        ),
                        rx.text(
                            "回覆一致性（0=很飄，10=很穩）",
                            size="2",
                            color="gray",
                            as_="span",
                        ),
                        rx.hstack(
                            rx.slider(
                                min=0,
                                max=10,
                                step=1,
                                value=[TargetState.response_consistency],
                                on_change=TargetState.set_response_consistency,
                                width="100%",
                                flex="1",
                                color_scheme="orange",
                            ),
                            rx.badge(TargetState.response_consistency, variant="soft"),
                            width="100%",
                            align="center",
                            spacing="3",
                        ),
                        rx.text("補充備註（選填）", size="2", color="gray", as_="span"),
                        rx.text_area(
                            value=TargetState.notes,
                            on_change=TargetState.set_notes,
                            placeholder="可記錄你願意交給系統分析的觀察重點。",
                            width="100%",
                            min_height="5rem",
                        ),
                        rx.button(
                            "儲存觀察對象",
                            on_click=TargetState.save_target,
                            width="100%",
                            size="4",
                            color_scheme="orange",
                        ),
                        rx.cond(
                            TargetState.status_message != "",
                            rx.callout(
                                TargetState.status_message,
                                icon="check",
                                color="green",
                                width="100%",
                            ),
                            rx.fragment(),
                        ),
                        spacing="3",
                        width="100%",
                        align_items="start",
                    ),
                    padding="1.25rem",
                    border_radius="16px",
                    width="100%",
                    max_width="28rem",
                    border="1px solid rgba(255,255,255,0.88)",
                    background="rgba(255,255,255,0.62)",
                ),
                rx.text(
                    "下一步：開始互動風險分析。",
                    size="2",
                    color="gray",
                    text_align="center",
                    as_="span",
                ),
                rx.link(
                    rx.button(
                        "開始分析",
                        variant="solid",
                        size="4",
                        width="100%",
                        max_width="28rem",
                        color_scheme="orange",
                    ),
                    href="/insight",
                    width="100%",
                ),
                rx.hstack(
                    rx.link(
                        rx.button("首頁", variant="ghost", size="3"),
                        href="/",
                    ),
                    rx.link(
                        rx.button("訊號檔案", variant="soft", size="3"),
                        href="/profile",
                    ),
                    spacing="3",
                    flex_wrap="wrap",
                    justify="center",
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
