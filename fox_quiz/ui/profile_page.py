from __future__ import annotations

import reflex as rx

from fox_quiz.state.profile_state import PROFILE_SAVE_SUCCESS_MESSAGE, ProfileState
from fox_quiz.ui.components.world_container import world_container


def profile_page() -> rx.Component:
    return world_container(
        rx.container(
            rx.vstack(
                rx.heading(
                    "建立你的訊號檔案",
                    size="7",
                    weight="bold",
                    text_align="center",
                ),
                rx.text(
                    "北極狐會根據你的習慣、興趣與壓力節奏，替你觀察容易消耗你的訊號。",
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
                            "你希望北極狐怎麼稱呼你",
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
                            "輸入你的興趣、生活習慣或長期關注的事",
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
                            "你最近的生活壓力程度（1-10）",
                            size="2",
                            color="gray",
                            as_="span",
                        ),
                        rx.input(
                            value=ProfileState.activity_text,
                            on_change=ProfileState.set_activity_text,
                            placeholder="5",
                            width="100%",
                            type="number",
                        ),
                        rx.text(
                            "完成後，北極狐會開始建立你的觀察模型。",
                            size="2",
                            color="gray",
                            text_align="center",
                            as_="span",
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
                        rx.link(
                            rx.button(
                                "前往觀察室",
                                size="4",
                                width="100%",
                                color_scheme="orange",
                            ),
                            href="/insight",
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
