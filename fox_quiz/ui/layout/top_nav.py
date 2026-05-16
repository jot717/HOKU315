from __future__ import annotations

import reflex as rx


def top_nav() -> rx.Component:
    return rx.hstack(
        rx.link("首頁", href="/"),
        rx.link("我的訊號", href="/profile"),
        rx.link("訊號問卷", href="/quiz"),
        rx.link("觀察對象", href="/target"),
        rx.link("分析結果", href="/insight"),
        rx.link("適合對象", href="/match"),
        spacing="6",
        padding="1em",
    )
