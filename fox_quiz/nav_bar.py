"""全域導航列：Phase1 核心迴圈 + 登入。"""
from __future__ import annotations

import reflex as rx

from fox_quiz.session_state import SessionState


def app_navbar(*, show_logout: bool = True) -> rx.Component:
    links = rx.hstack(
        rx.link("首頁", href="/", size="2", color="gray"),
        rx.link("我的訊號", href="/profile", size="2", color="orange", font_weight="medium"),
        rx.link("訊號問卷", href="/quiz", size="2", color="gray"),
        rx.link("觀察對象", href="/target", size="2", color="orange", font_weight="medium"),
        rx.link("分析結果", href="/insight", size="2", color="orange", font_weight="medium"),
        rx.link("適合對象", href="/match", size="2", color="orange", font_weight="medium"),
        rx.link("帳號登入", href="/login", size="2", color="gray"),
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
