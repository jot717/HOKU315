"""Task 7：北極狐配對牆（UAT-04 門檻：0.7 模糊、1.2 攔截）。"""
from __future__ import annotations

import asyncio
import os
from typing import Any

import reflex as rx

import db_service
from fox_quiz.session_state import SessionState

_BG = "linear-gradient(180deg, #f8fafc 0%, #e0f2fe 100%)"
_PLACEHOLDER_IMG = "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=800&auto=format&fit=crop"
_STORAGE_PUBLIC_BASE = f"{(os.getenv('SUPABASE_URL') or '').strip().rstrip('/')}/storage/v1/object/public"


class MatchWallState(rx.State):
    matches: list[dict[str, Any]] = []
    blocked_count: int = 0
    loading: bool = False
    error_msg: str = ""

    @rx.event
    async def load_match_wall(self) -> Any:
        sess = await self.get_state(SessionState)
        token = (sess.access_token or "").strip()
        if not token:
            return rx.redirect("/login")

        async with self:
            self.loading = True
            self.error_msg = ""

        def _load() -> tuple[list[dict[str, Any]], int]:
            db_service.ensure_user_profile(token)
            rows = db_service.get_safe_matches_current_user(token)
            out: list[dict[str, Any]] = []
            for r in rows:
                path = str(r.get("image_object_path") or "").strip()
                bucket = str(r.get("image_bucket") or "stories").strip() or "stories"
                image_url = (
                    f"{_STORAGE_PUBLIC_BASE}/{bucket}/{path}"
                    if _STORAGE_PUBLIC_BASE and path
                    else _PLACEHOLDER_IMG
                )
                nr = dict(r)
                nr["image_url"] = image_url
                out.append(nr)
            blocked = int(rows[0].get("blocked_count", 0)) if rows else 0
            return out, blocked

        try:
            rows, blocked = await asyncio.to_thread(_load)
        except Exception as e:
            async with self:
                self.loading = False
                self.matches = []
                self.blocked_count = 0
                self.error_msg = f"配對牆載入失敗：{e}"
            return

        async with self:
            self.loading = False
            self.matches = rows
            self.blocked_count = blocked
            self.error_msg = ""


def _match_card(item: dict[str, Any]) -> rx.Component:
    is_blurred = item["is_blurred"]
    distance = item["distance"]
    dim_label = item["conflict_dim_label"]
    image_url = item["image_url"]
    return rx.card(
        rx.vstack(
            rx.cond(
                is_blurred,
                rx.image(
                    src=image_url,
                    width="100%",
                    height="180px",
                    object_fit="cover",
                    border_radius="12px",
                    style={"filter": "blur(30px)"},
                ),
                rx.image(
                    src=image_url,
                    width="100%",
                    height="180px",
                    object_fit="cover",
                    border_radius="12px",
                ),
            ),
            rx.hstack(
                rx.badge(
                    rx.text("距離 ", distance),
                    color_scheme="orange",
                    variant="surface",
                ),
                rx.badge(
                    rx.cond(is_blurred, "模糊預警", "可見"),
                    color_scheme=rx.cond(is_blurred, "red", "green"),
                    variant="soft",
                ),
                width="100%",
            ),
            rx.cond(
                is_blurred,
                rx.text(f"預警維度：{dim_label}", size="2", color="red"),
                rx.text(f"主要落差：{dim_label}", size="2", color="gray"),
            ),
            rx.button(
                "詳情（Task 8 解鎖）",
                disabled=is_blurred,
                variant="outline",
                size="2",
                width="100%",
            ),
            spacing="3",
            width="100%",
            align_items="start",
        ),
        width="100%",
    )


def match_wall_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.link("← 首頁", href="/", color="orange", weight="medium"),
                rx.spacer(),
                rx.button("登出", on_click=SessionState.sign_out, variant="soft", size="2"),
                width="100%",
            ),
            rx.heading("北極狐配對牆", size="6", weight="bold"),
            rx.card(
                rx.text(
                    f"守護中：已為您成功攔截 {MatchWallState.blocked_count} 個高風險地雷。",
                    size="3",
                    weight="bold",
                ),
                width="100%",
                background="rgba(255, 237, 213, 0.65)",
            ),
            rx.hstack(
                rx.button(
                    rx.cond(MatchWallState.loading, "載入中…", "刷新配對牆"),
                    on_click=MatchWallState.load_match_wall,
                    color_scheme="orange",
                    disabled=MatchWallState.loading,
                ),
                width="100%",
            ),
            rx.cond(
                MatchWallState.error_msg != "",
                rx.callout(
                    MatchWallState.error_msg,
                    icon="triangle-alert",
                    color="red",
                    width="100%",
                ),
                rx.box(),
            ),
            rx.cond(
                MatchWallState.matches != [],
                rx.grid(
                    rx.foreach(MatchWallState.matches, _match_card),
                    columns=rx.breakpoints(initial="1", sm="2", md="3"),
                    spacing="4",
                    width="100%",
                ),
                rx.text(
                    "目前沒有可顯示對象（高風險已攔截或資料尚未建立）。",
                    size="2",
                    color="gray",
                    width="100%",
                ),
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
