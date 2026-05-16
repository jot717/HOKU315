from __future__ import annotations

import reflex as rx

from fox_quiz.state.profile_state import PROFILE_SAVE_SUCCESS_MESSAGE, ProfileState
from fox_quiz.ui.components.world_container import world_container


def profile_page() -> rx.Component:
    return world_container(
        rx.container(
            rx.vstack(
                rx.heading(
                    "建立你的社交訊號檔案",
                    size="7",
                    weight="bold",
                    text_align="center",
                ),
                rx.text(
                    "系統會根據你的社交節奏、壓力耐受度與互動偏好，建立你的基礎互動模型。",
                    size="2",
                    color="gray",
                    text_align="center",
                    max_width="28rem",
                    as_="span",
                ),
                rx.box(
                    rx.vstack(
                        rx.text(
                            "這會影響：\n"
                            "- 危險互動分析\n"
                            "- 情緒消耗判定\n"
                            "- 社交節奏分析\n"
                            "- 適合對象推薦",
                            size="3",
                            color="gray",
                            text_align="left",
                            style={"line_height": "1.75", "white_space": "pre-wrap"},
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
                    border="1px solid rgba(255,255,255,0.88)",
                    background="rgba(255,255,255,0.62)",
                ),
                rx.box(
                    rx.vstack(
                        rx.text(
                            "系統如何稱呼你",
                            size="2",
                            color="gray",
                            as_="span",
                        ),
                        rx.input(
                            value=ProfileState.name,
                            on_change=ProfileState.set_name,
                            placeholder="例如：小安",
                            width="100%",
                        ),
                        rx.text(
                            "你的興趣、生活型態與長期關注事物",
                            size="2",
                            color="gray",
                            as_="span",
                        ),
                        rx.input(
                            value=ProfileState.interests_text,
                            on_change=ProfileState.set_interests_text,
                            placeholder="閱讀, 散步, 音樂（以逗號分隔）",
                            width="100%",
                        ),
                        rx.text(
                            "你目前的社交與生活壓力程度",
                            size="2",
                            color="gray",
                            as_="span",
                        ),
                        rx.input(
                            value=ProfileState.activity_text,
                            on_change=ProfileState.set_activity_text,
                            placeholder="1–10",
                            width="100%",
                            type="number",
                        ),
                        rx.button(
                            "儲存訊號檔案",
                            on_click=ProfileState.save_profile,
                            size="3",
                            width="100%",
                            color_scheme="orange",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    padding="1.5rem",
                    border_radius="18px",
                    width="100%",
                    max_width="28rem",
                    border="1px solid rgba(255,255,255,0.92)",
                    background="rgba(255,255,255,0.78)",
                    style={"boxShadow": "0 10px 36px rgba(155, 185, 215, 0.12)"},
                ),
                rx.cond(
                    ProfileState.status_message == PROFILE_SAVE_SUCCESS_MESSAGE,
                    rx.vstack(
                        rx.callout(
                            PROFILE_SAVE_SUCCESS_MESSAGE,
                            icon="check",
                            color="green",
                            width="100%",
                        ),
                        rx.heading(
                            "下一步",
                            size="4",
                            weight="medium",
                            width="100%",
                            text_align="center",
                        ),
                        rx.text(
                            "繼續完成社交訊號問卷，讓系統更準確理解你的互動模式。",
                            size="2",
                            color="gray",
                            text_align="center",
                            as_="span",
                        ),
                        rx.link(
                            rx.button(
                                "開始訊號問卷",
                                size="4",
                                width="100%",
                                color_scheme="orange",
                            ),
                            href="/quiz",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                        max_width="28rem",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    ProfileState.status_message != "",
                    rx.cond(
                        ProfileState.status_message != PROFILE_SAVE_SUCCESS_MESSAGE,
                        rx.callout(
                            ProfileState.status_message,
                            icon="triangle-alert",
                            color="amber",
                            width="100%",
                            max_width="28rem",
                        ),
                        rx.fragment(),
                    ),
                    rx.fragment(),
                ),
                spacing="6",
                align="center",
                width="100%",
            ),
            padding_y="3rem",
            padding_x="1.25rem",
            width="100%",
        ),
    )
