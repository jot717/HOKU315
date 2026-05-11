from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState
from fox_quiz.ui.components.fox_message_card import fox_message_card
from fox_quiz.ui.components.hero_insight import hero_insight
from fox_quiz.ui.components.insight_cards import insight_cards
from fox_quiz.ui.components.session_history import session_history


def _loading_banner() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.spinner(size="3"),
            rx.text(
                "北極狐正在為你整理訊號，請稍候片刻…",
                size="3",
                weight="medium",
                as_="span",
            ),
            spacing="3",
            align="center",
            width="100%",
            justify="center",
        ),
        padding="1rem",
        border_radius="12px",
        width="100%",
        background="var(--accent-3)",
        border="1px solid var(--accent-6)",
    )


def _empty_state() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                "北極狐正在等待你的訊號",
                size="5",
                weight="medium",
                text_align="center",
                as_="span",
            ),
            rx.text(
                "有些疲憊，不需要自己承受。",
                size="3",
                color="gray",
                text_align="center",
                style={"line_height": "1.6"},
                as_="span",
            ),
            rx.button(
                "開始觀察",
                on_click=AppState.run_demo_match,
                size="4",
                width="100%",
                color_scheme="orange",
                disabled=AppState.demo_match_loading,
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        padding="2.5rem",
        width="100%",
        border_radius="16px",
        border="1px solid var(--gray-6)",
        background="var(--gray-2)",
    )


def _onboarding_strip() -> rx.Component:
    return rx.box(
        rx.text(
            "先留下你的輪廓，再請北極狐觀察訊號——示範流程，不需額外設定。",
            size="2",
            color="gray",
            text_align="center",
            style={"line_height": "1.55"},
            as_="span",
        ),
        padding_x="0.5rem",
        padding_bottom="1rem",
        width="100%",
    )


def insight_panel() -> rx.Component:
    return rx.vstack(
        _onboarding_strip(),
        rx.cond(AppState.demo_match_loading, _loading_banner(), rx.fragment()),
        rx.cond(
            AppState.has_insight,
            rx.vstack(
                hero_insight(),
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "解析摘要",
                            size="4",
                            weight="medium",
                        ),
                        rx.text(
                            AppState.insight_ai_summary,
                            size="3",
                            style={"line_height": "1.65"},
                            as_="span",
                        ),
                        rx.heading(
                            "共同特質",
                            size="3",
                            weight="medium",
                            margin_top="3",
                        ),
                        rx.text(
                            AppState.insight_shared_traits_text,
                            size="3",
                            color="gray",
                            style={"line_height": "1.65"},
                            as_="span",
                        ),
                        rx.heading(
                            "活動節奏分析",
                            size="3",
                            weight="medium",
                            margin_top="3",
                        ),
                        rx.text(
                            AppState.insight_activity_analysis,
                            size="3",
                            style={"line_height": "1.65"},
                            as_="span",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    padding="1.25rem",
                    border_radius="12px",
                    width="100%",
                    border="1px solid var(--gray-6)",
                    background="var(--gray-1)",
                ),
                fox_message_card(AppState.fox_message),
                insight_cards(),
                rx.cond(
                    AppState.show_final_card,
                    session_history(),
                ),
                spacing="6",
                width="100%",
            ),
            _empty_state(),
        ),
        rx.vstack(
            rx.text(
                "更多操作",
                size="2",
                weight="bold",
                color="gray",
                as_="span",
            ),
            rx.hstack(
                rx.button(
                    "載入上次解析",
                    on_click=AppState.load_latest_session,
                    variant="soft",
                    size="2",
                    disabled=AppState.demo_match_loading,
                ),
                rx.cond(
                    AppState.has_insight,
                    rx.button(
                        "再次觀察",
                        on_click=AppState.run_demo_match,
                        variant="outline",
                        size="2",
                        color_scheme="orange",
                        disabled=AppState.demo_match_loading,
                    ),
                    rx.fragment(),
                ),
                rx.button(
                    "更新紀錄",
                    on_click=AppState.load_session_history,
                    variant="ghost",
                    size="2",
                    disabled=AppState.demo_match_loading,
                ),
                spacing="3",
                width="100%",
                flex_wrap="wrap",
            ),
            spacing="2",
            width="100%",
            align="start",
        ),
        spacing="6",
        width="100%",
        align="center",
    )
