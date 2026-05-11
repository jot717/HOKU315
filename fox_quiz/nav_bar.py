"""全域導航列：Story / Match / Unlocks。"""
from __future__ import annotations

import reflex as rx

from fox_quiz.session_state import SessionState


def app_navbar(*, show_logout: bool = True) -> rx.Component:
    links = rx.hstack(
        rx.link("登入", href="/login", size="2", color="gray"),
        rx.link("訊號牆", href="/match", size="2", color="orange", font_weight="medium"),
        rx.link("故事", href="/story", size="2", color="orange", font_weight="medium"),
        rx.link("解鎖", href="/unlocks", size="2", color="orange", font_weight="medium"),
        rx.link("測驗", href="/quiz", size="2", color="gray"),
        spacing="4",
        flex_wrap="wrap",
    )
    if show_logout:
        return rx.hstack(
            links,
            rx.spacer(),
            rx.button("登出", on_click=SessionState.sign_out, variant="soft", size="2"),
            width="100%",
            align="center",
            spacing="4",
        )
    return rx.hstack(links, width="100%", spacing="4")
