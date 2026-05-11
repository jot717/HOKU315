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


def insight_onboarding_explanation_card() -> rx.Component:
    """Shown before the user runs observation (empty state)."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "北極狐正在觀察",
                size="5",
                weight="medium",
                text_align="center",
            ),
            rx.text(
                "北極狐會：",
                size="3",
                weight="medium",
                as_="span",
            ),
            rx.text(
                "1. 觀察你的訊號節奏\n"
                "2. 找出容易消耗你的模式\n"
                "3. 幫你提前避開危險互動",
                size="3",
                color="gray",
                style={"line_height": "1.75", "white_space": "pre-wrap"},
                as_="span",
            ),
            spacing="3",
            width="100%",
            align="center",
        ),
        padding="1.5rem",
        border_radius="18px",
        width="100%",
        border="1px solid rgba(255,255,255,0.92)",
        background="rgba(255,255,255,0.78)",
        style={"boxShadow": "0 10px 36px rgba(155, 185, 215, 0.12)"},
    )


def insight_result_explanation_section() -> rx.Component:
    """Post-result explainability (guardian framing, no dating language)."""
    risk_block = rx.cond(
        AppState.signal_risk_flag_lines != "",
        rx.text(
            AppState.signal_risk_flag_lines,
            size="3",
            color="gray",
            style={"line_height": "1.75", "white_space": "pre-wrap"},
            as_="span",
        ),
        rx.text(
            "目前沒有額外的高風險標記；北極狐仍建議維持你覺得舒服的距離。",
            size="3",
            color="gray",
            style={"line_height": "1.75"},
            as_="span",
        ),
    )
    return rx.box(
        rx.vstack(
            rx.heading(
                "為什麼會出現這個結果？",
                size="4",
                weight="medium",
            ),
            rx.text(
                "哪些訊號造成風險",
                size="2",
                weight="bold",
                color="gray",
                as_="span",
            ),
            risk_block,
            rx.text(
                "哪些模式正在重複",
                size="2",
                weight="bold",
                color="gray",
                margin_top="3",
                as_="span",
            ),
            rx.text(
                AppState.recurring_pattern,
                size="3",
                color="gray",
                style={"line_height": "1.75"},
                as_="span",
            ),
            rx.text(
                "北極狐建議避開什麼",
                size="2",
                weight="bold",
                color="gray",
                margin_top="3",
                as_="span",
            ),
            rx.text(
                AppState.guardian_warning,
                size="3",
                color="gray",
                style={"line_height": "1.75"},
                as_="span",
            ),
            spacing="3",
            width="100%",
            align_items="start",
        ),
        padding="1.5rem",
        border_radius="18px",
        width="100%",
        border="1px solid rgba(255,255,255,0.95)",
        background="rgba(255,255,255,0.85)",
        style={"boxShadow": "0 10px 36px rgba(150, 175, 210, 0.1)"},
    )


def insight_next_actions_section() -> rx.Component:
    """Clear next steps after a result."""
    return rx.box(
        rx.vstack(
            rx.text(
                "下一步",
                size="2",
                weight="bold",
                color="gray",
                as_="span",
            ),
            rx.hstack(
                rx.button(
                    "重新觀察",
                    on_click=AppState.run_demo_match,
                    variant="outline",
                    size="3",
                    color_scheme="orange",
                    disabled=AppState.demo_match_loading,
                ),
                rx.link(
                    rx.button(
                        "更新我的訊號",
                        variant="soft",
                        size="3",
                    ),
                    href="/profile",
                ),
                rx.button(
                    "查看北極狐筆記",
                    on_click=AppState.load_session_history,
                    variant="ghost",
                    size="3",
                    disabled=AppState.demo_match_loading,
                ),
                spacing="3",
                width="100%",
                flex_wrap="wrap",
                justify="center",
            ),
            spacing="3",
            width="100%",
            align="center",
        ),
        padding="1.25rem",
        border_radius="16px",
        width="100%",
        border="1px dashed rgba(160, 185, 215, 0.55)",
        background="rgba(255,255,255,0.55)",
    )


def _loading_banner() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.spinner(size="3"),
            rx.text(
                "北極狐正在替你檢查危險訊號",
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
            insight_onboarding_explanation_card(),
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
            "這裡是觀察室：北極狐會讀你的訊號檔案，並用守護視角整理你附近的壓力來源。示範流程，不需額外設定。",
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
                insight_result_explanation_section(),
                insight_next_actions_section(),
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
