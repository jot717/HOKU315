from __future__ import annotations

import reflex as rx

from fox_quiz.state.app_state import AppState


def insight_onboarding_explanation_card() -> rx.Component:
    """Shown before the user runs observation (empty state)."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "互動壓力分析",
                size="5",
                weight="medium",
                text_align="center",
            ),
            rx.text(
                "建議流程：訊號檔案（/profile）→ 訊號問卷（/quiz）→ 觀察對象（/target）→ 在此執行分析。"
                "系統會解讀「哪種互動節奏在耗你」，而不是給性格標籤。",
                size="2",
                color="gray",
                text_align="center",
                style={"line_height": "1.65"},
                max_width="28rem",
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


def insight_pressure_section() -> rx.Component:
    """Why this interaction shape drains you — causal bullets."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "為何會耗竭",
                size="4",
                weight="medium",
            ),
            rx.cond(
                AppState.ux_why_drains_line != "",
                rx.text(
                    AppState.ux_why_drains_line,
                    size="3",
                    color="gray",
                    style={"line_height": "1.65"},
                    as_="span",
                ),
                rx.text(
                    AppState.energy_summary,
                    size="3",
                    color="gray",
                    style={"line_height": "1.65"},
                    as_="span",
                ),
            ),
            rx.cond(
                AppState.ux_pressure_bullets_formatted != "",
                rx.text(
                    AppState.ux_pressure_bullets_formatted,
                    size="2",
                    color="gray",
                    style={"line_height": "1.65", "white_space": "pre-wrap"},
                    as_="span",
                ),
                rx.fragment(),
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


def insight_why_bullets_section() -> rx.Component:
    """Regression alias for Phase1 UAT tests."""
    return insight_pressure_section()


def insight_result_explanation_section() -> rx.Component:
    """Regression alias."""
    return insight_pressure_section()


def insight_next_actions_section() -> rx.Component:
    """Next steps after a result."""
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
                    "重新分析",
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
                rx.link(
                    rx.button(
                        "查看適合對象",
                        variant="solid",
                        size="4",
                        width="100%",
                        color_scheme="orange",
                    ),
                    href="/match",
                    width="100%",
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


def _row_item(label: str, body) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="1", color="gray", weight="bold", as_="span"),
        body,
        spacing="1",
        align_items="start",
        width="100%",
    )


def _section_result_summary() -> rx.Component:
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
            rx.heading(
                "互動分析結果",
                size="5",
                weight="bold",
            ),
            _row_item(
                "節奏衝突",
                rx.text(
                    AppState.insight_communication_rhythm_line,
                    size="3",
                    color="gray",
                    style={"line_height": "1.65"},
                    as_="span",
                ),
            ),
            _row_item("整體危險度", risk_callout),
            rx.text(
                AppState.insight_target_summary_line,
                size="2",
                color="gray",
                style={"line_height": "1.6"},
                as_="span",
            ),
            rx.text(
                "此結果為規則式互動壓力解讀，非心理診斷或醫療建議。",
                size="1",
                color="gray",
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
        background="rgba(255,255,255,0.88)",
        style={"boxShadow": "0 12px 40px rgba(160, 185, 215, 0.14)"},
    )


def _section_best_social_fit() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                "為何這種相處較省力",
                size="4",
                weight="medium",
            ),
            rx.cond(
                AppState.ux_fit_reasoning != "",
                rx.text(
                    AppState.ux_fit_reasoning,
                    size="3",
                    color="gray",
                    style={"line_height": "1.65"},
                    as_="span",
                ),
                rx.cond(
                    AppState.has_relationship_explanation_lines,
                    rx.text(
                        AppState.relationship_explanation_bullets_formatted,
                        size="3",
                        color="gray",
                        style={"line_height": "1.65", "white_space": "pre-wrap"},
                        as_="span",
                    ),
                    rx.text(
                        AppState.compatibility_title,
                        size="3",
                        color="gray",
                        style={"line_height": "1.65"},
                        as_="span",
                    ),
                ),
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


def _section_avoid_types() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                "建議先拉開的互動形狀",
                size="4",
                weight="medium",
            ),
            rx.cond(
                AppState.ux_avoid_reasoning != "",
                rx.text(
                    AppState.ux_avoid_reasoning,
                    size="3",
                    color="gray",
                    style={"line_height": "1.65"},
                    as_="span",
                ),
                rx.cond(
                    AppState.has_signal_inference_types,
                    rx.text(
                        AppState.signal_inference_bullets_formatted,
                        size="3",
                        color="gray",
                        style={"line_height": "1.65", "white_space": "pre-wrap"},
                        as_="span",
                    ),
                    rx.text(
                        AppState.relationship_archetype_danger_summary,
                        size="3",
                        color="gray",
                        style={"line_height": "1.65"},
                        as_="span",
                    ),
                ),
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
        background="rgba(255,255,255,0.78)",
        style={"boxShadow": "0 10px 32px rgba(160, 185, 210, 0.1)"},
    )


def _section_fox_observer() -> rx.Component:
    """Single fox block — quiet observer only."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "北極狐觀察",
                size="4",
                weight="medium",
            ),
            rx.cond(
                AppState.ux_fox_observer_note != "",
                rx.text(
                    AppState.ux_fox_observer_note,
                    size="3",
                    color="gray",
                    style={"line_height": "1.65", "white_space": "pre-wrap"},
                    as_="span",
                ),
                rx.text(
                    AppState.fox_message,
                    size="3",
                    color="gray",
                    style={"line_height": "1.65", "white_space": "pre-wrap"},
                    as_="span",
                ),
            ),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        padding="1.25rem",
        border_radius="16px",
        width="100%",
        max_width="32rem",
        border="1px dashed rgba(180, 200, 230, 0.7)",
        background="rgba(255,255,255,0.65)",
    )


def _insight_result_column() -> rx.Component:
    return rx.vstack(
        _section_result_summary(),
        insight_pressure_section(),
        _section_best_social_fit(),
        _section_avoid_types(),
        _section_fox_observer(),
        insight_next_actions_section(),
        spacing="6",
        width="100%",
        align="center",
    )


def _loading_banner() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.spinner(size="3"),
            rx.text(
                "系統正在解讀互動壓力與節奏…",
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
                "按下開始後，系統會說明哪些互動節奏在消耗你，以及為何。",
                size="3",
                color="gray",
                text_align="center",
                style={"line_height": "1.6"},
                as_="span",
            ),
            rx.button(
                "開始分析",
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
            "此頁解讀互動壓力與節奏，幫你看見「為什麼會累」，而不是貼標籤。",
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


def _pre_insight_column() -> rx.Component:
    return rx.vstack(
        _onboarding_strip(),
        rx.cond(AppState.demo_match_loading, _loading_banner(), rx.fragment()),
        _empty_state(),
        spacing="5",
        width="100%",
        align="center",
    )


def insight_panel() -> rx.Component:
    return rx.vstack(
        rx.cond(
            AppState.has_insight,
            _insight_result_column(),
            _pre_insight_column(),
        ),
        spacing="7",
        width="100%",
        align="center",
    )
