"""Task 9 前置：解鎖／付費占位頁。"""
from __future__ import annotations

import reflex as rx

from fox_quiz.nav_bar import app_navbar

_BG = "linear-gradient(180deg, #fafafa 0%, #fff7ed 100%)"


def unlocks_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            app_navbar(),
            rx.heading("解鎖中心", size="6", weight="bold"),
            rx.text(
                "此頁為占位：完整支付與攻略交付見 BACKLOG Task 8／Task 9。",
                size="2",
                color="gray",
                as_="span",
                display="block",
            ),
            spacing="4",
            width="100%",
            max_width="40rem",
            padding="6",
        ),
        min_height="100vh",
        width="100%",
        background=_BG,
    )
