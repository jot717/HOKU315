from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState
from fox_quiz.ui.components.fox_avatar import fox_avatar
from fox_quiz.ui.components.fox_memory_card import fox_memory_card
from fox_quiz.ui.components.fox_message_card import fox_message_card
from fox_quiz.ui.components.hero_insight import hero_insight
from fox_quiz.ui.components.insight_cards import insight_cards
from fox_quiz.ui.components.session_history import session_history
from fox_quiz.ui.components.signal_guard_card import signal_guard_card
from fox_quiz.ui.components.signal_scan_banner import signal_scan_banner


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
        background="rgba(255,255,255,0.65)",
        border="1px solid rgba(255,255,255,0.9)",
        style={"boxShadow": "0 6px 24px rgba(150, 180, 220, 0.12)"},
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
            spacing="5",
            align="center",
            width="100%",
        ),
        padding="2.75rem",
        width="100%",
        border_radius="20px",
        border="1px solid rgba(255,255,255,0.9)",
        background="rgba(255,255,255,0.72)",
        style={"boxShadow": "0 12px 40px rgba(160, 185, 215, 0.14)"},
    )


def _onboarding_strip() -> rx.Component:
    return rx.box(
        rx.text(
            "走進安靜的觀察室，留下輪廓後，請北極狐替你讀訊號。示範流程，不需額外設定。",
            size="2",
            color="gray",
            text_align="center",
            style={"line_height": "1.65"},
            as_="span",
        ),
        padding_x="0.5rem",
        padding_bottom="1rem",
        width="100%",
    )


def insight_panel() -> rx.Component:
    return rx.vstack(
        fox_avatar(),
        fox_memory_card(AppState.fox_memory_note, AppState.recurring_pattern),
        signal_guard_card(
            AppState.signal_risk_level,
            AppState.signal_risk_flags,
            AppState.guardian_warning,
        ),
        signal_scan_banner(),
        _onboarding_strip(),
        rx.cond(AppState.demo_match_loading, _loading_banner(), rx.fragment()),
        rx.cond(
            AppState.has_insight,
            rx.vstack(
                hero_insight(),
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "觀察筆記",
                            size="4",
                            weight="medium",
                        ),
                        rx.text(
                            AppState.insight_ai_summary,
                            size="3",
                            style={"line_height": "1.75"},
                            as_="span",
                        ),
                        rx.heading(
                            "相似的痕跡",
                            size="3",
                            weight="medium",
                            margin_top="4",
                        ),
                        rx.text(
                            AppState.insight_shared_traits_text,
                            size="3",
                            color="gray",
                            style={"line_height": "1.75"},
                            as_="span",
                        ),
                        rx.heading(
                            "節奏與壓力",
                            size="3",
                            weight="medium",
                            margin_top="4",
                        ),
                        rx.text(
                            AppState.insight_activity_analysis,
                            size="3",
                            style={"line_height": "1.75"},
                            as_="span",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    padding="1.5rem",
                    border_radius="18px",
                    width="100%",
                    border="1px solid rgba(255,255,255,0.95)",
                    background="rgba(255,255,255,0.82)",
                    style={"boxShadow": "0 10px 36px rgba(150, 175, 210, 0.1)"},
                ),
                fox_message_card(AppState.fox_message),
                insight_cards(),
                rx.cond(
                    AppState.show_final_card,
                    session_history(),
                ),
                spacing="7",
                width="100%",
            ),
            _empty_state(),
        ),
        rx.vstack(
            rx.text(
                "守護選單",
                size="2",
                weight="bold",
                color="gray",
                as_="span",
            ),
            rx.hstack(
                rx.button(
                    "載入上次觀察",
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
            spacing="3",
            width="100%",
            align="start",
        ),
        spacing="7",
        width="100%",
        align="center",
    )
