from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState
from fox_quiz.ui.components.fox_avatar import fox_avatar


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
                "建議先在「訊號檔案」頁存好你的節奏；這裡讀的是同一套訊號，不是另一套問卷。",
                size="2",
                color="gray",
                text_align="center",
                style={"line_height": "1.65"},
                max_width="28rem",
                as_="span",
            ),
            rx.text(
                "北極狐會：",
                size="3",
                weight="medium",
                as_="span",
            ),
            rx.text(
                "1. 替你擋掉容易消耗的訊號\n"
                "2. 提醒你在太累以前先休息\n"
                "3. 用守護視角陪你整理壓力",
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


def insight_why_bullets_section() -> rx.Component:
    """Section 3 — short bullets only (max 3 from state)."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "為什麼會這樣？",
                size="4",
                weight="medium",
            ),
            rx.foreach(
                AppState.guardian_why_lines,
                lambda line: rx.hstack(
                    rx.text("・", size="3", color="gray", as_="span"),
                    rx.text(
                        line,
                        size="3",
                        color="gray",
                        style={"line_height": "1.65"},
                        as_="span",
                    ),
                    spacing="1",
                    align="start",
                    width="100%",
                ),
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


def insight_result_explanation_section() -> rx.Component:
    """Regression alias: post-result WHY (bullets only, guardian tone)."""
    return insight_why_bullets_section()


def insight_next_actions_section() -> rx.Component:
    """Section 5 — clear next steps after a result."""
    return rx.box(
        rx.vstack(
            rx.text(
                "下一步",
                size="3",
                weight="bold",
                color="gray",
                as_="span",
            ),
            rx.vstack(
                rx.button(
                    "重新觀察",
                    on_click=AppState.run_demo_match,
                    variant="outline",
                    size="4",
                    width="100%",
                    color_scheme="orange",
                    disabled=AppState.demo_match_loading,
                ),
                rx.link(
                    rx.button(
                        "更新我的訊號",
                        variant="soft",
                        size="4",
                        width="100%",
                    ),
                    href="/profile",
                    width="100%",
                ),
                rx.button(
                    "查看守護筆記",
                    on_click=AppState.load_session_history,
                    variant="ghost",
                    size="4",
                    width="100%",
                    disabled=AppState.demo_match_loading,
                ),
                spacing="3",
                width="100%",
            ),
            spacing="3",
            width="100%",
            align="center",
        ),
        padding="1.5rem",
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
                "按下開始，北極狐會陪你看一眼附近的訊號。",
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
            "這裡是觀察室：北極狐讀你的訊號檔案，用守護視角幫你過濾壓力來源。示範流程，不需額外設定。",
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


def _section_fox_guardian_presence() -> rx.Component:
    risk_callout = rx.cond(
        AppState.display_risk_level == "high",
        rx.callout(
            AppState.guardian_risk_status_short,
            icon="triangle-alert",
            color="red",
            width="100%",
        ),
        rx.cond(
            AppState.display_risk_level == "medium",
            rx.callout(
                AppState.guardian_risk_status_short,
                icon="triangle-alert",
                color="amber",
                width="100%",
            ),
            rx.callout(
                AppState.guardian_risk_status_short,
                icon="check",
                color="green",
                width="100%",
            ),
        ),
    )
    return rx.box(
        rx.vstack(
            fox_avatar(),
            rx.heading(
                AppState.guardian_presence_line_primary,
                size="5",
                weight="medium",
                text_align="center",
                style={"line_height": "1.45"},
            ),
            rx.text(
                AppState.guardian_interaction_framing,
                size="3",
                color="gray",
                text_align="center",
                style={"line_height": "1.65"},
                as_="span",
            ),
            risk_callout,
            rx.text(
                AppState.guardian_warning,
                size="3",
                color="gray",
                text_align="center",
                style={"line_height": "1.7"},
                as_="span",
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        padding="2.25rem",
        width="100%",
        max_width="32rem",
        border_radius="22px",
        border="1px solid rgba(255,255,255,0.95)",
        background="rgba(255,255,255,0.88)",
        style={"boxShadow": "0 14px 44px rgba(155, 185, 215, 0.16)"},
    )


def _section_archetype_vigilance() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                "北極狐正在警戒的互動類型（示範）",
                size="3",
                weight="bold",
                as_="span",
            ),
            rx.text(
                AppState.relationship_archetype_name,
                size="4",
                weight="medium",
                as_="span",
            ),
            rx.hstack(
                rx.badge(
                    AppState.relationship_archetype_pressure,
                    color_scheme="orange",
                    variant="soft",
                ),
                rx.text(
                    "互動壓力指數",
                    size="1",
                    color="gray",
                    as_="span",
                ),
                rx.text(
                    AppState.relationship_interaction_risk_score,
                    size="2",
                    weight="bold",
                    as_="span",
                ),
                spacing="2",
                align="center",
            ),
            rx.text(
                AppState.relationship_archetype_danger_summary,
                size="2",
                color="gray",
                style={"line_height": "1.65"},
                as_="span",
            ),
            rx.text(
                AppState.relationship_archetype_guardian_hint,
                size="2",
                color="gray",
                style={"line_height": "1.6"},
                as_="span",
            ),
            rx.text(
                AppState.guardian_simulation_advice,
                size="2",
                weight="medium",
                style={"line_height": "1.6"},
                as_="span",
            ),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        padding="1.25rem",
        border_radius="14px",
        width="100%",
        max_width="32rem",
        border="1px solid rgba(200, 215, 240, 0.65)",
        background="rgba(255,255,255,0.72)",
    )


def _section_danger_pattern() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                "北極狐看到的危險型態",
                size="2",
                weight="bold",
                color="gray",
                as_="span",
            ),
            rx.text(
                AppState.inference_high_warning,
                size="3",
                weight="medium",
                style={"line_height": "1.65"},
                as_="span",
            ),
            rx.text(
                "這不是心理診斷，而是依你輸入的訊號組合做的規則式提醒。",
                size="1",
                color="gray",
                style={"line_height": "1.55"},
                as_="span",
            ),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        padding="1.25rem",
        border_radius="14px",
        width="100%",
        max_width="32rem",
        border="1px solid rgba(255,200,160,0.45)",
        background="rgba(255,248,240,0.75)",
    )


def _section_main_warning() -> rx.Component:
    return rx.box(
        rx.heading(
            AppState.guardian_main_warning_title,
            size="7",
            weight="bold",
            text_align="center",
            style={"line_height": "1.25"},
        ),
        padding_y="0.5rem",
        width="100%",
        max_width="32rem",
    )


def _section_fox_guidance() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                "北極狐的建議",
                size="4",
                weight="medium",
            ),
            rx.text(
                AppState.guardian_action_display,
                size="4",
                style={"line_height": "1.65"},
                as_="span",
            ),
            spacing="3",
            width="100%",
            align_items="start",
        ),
        padding="1.5rem",
        border_radius="18px",
        width="100%",
        max_width="32rem",
        border="1px solid rgba(255,255,255,0.92)",
        background="rgba(255,255,255,0.8)",
        style={"boxShadow": "0 10px 32px rgba(160, 185, 210, 0.12)"},
    )


def _guardian_insight_result_column() -> rx.Component:
    return rx.vstack(
        _section_fox_guardian_presence(),
        _section_danger_pattern(),
        _section_archetype_vigilance(),
        _section_main_warning(),
        insight_why_bullets_section(),
        _section_fox_guidance(),
        insight_next_actions_section(),
        spacing="6",
        width="100%",
        align="center",
    )


def _pre_insight_column() -> rx.Component:
    return rx.vstack(
        _onboarding_strip(),
        rx.cond(AppState.demo_match_loading, _loading_banner(), rx.fragment()),
        _empty_state(),
        spacing="5",
        width="100%",
        align="center",
    )


def _footer_menu() -> rx.Component:
    return rx.box(
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
                justify="center",
            ),
            spacing="3",
            width="100%",
            align="center",
        ),
        padding_top="1rem",
        width="100%",
        max_width="28rem",
    )


def insight_panel() -> rx.Component:
    return rx.vstack(
        rx.cond(
            AppState.has_insight,
            _guardian_insight_result_column(),
            _pre_insight_column(),
        ),
        _footer_menu(),
        spacing="7",
        width="100%",
        align="center",
    )
