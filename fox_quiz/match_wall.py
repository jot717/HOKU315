"""Task 7：北極狐配對牆（UAT-04 門檻：0.7 模糊、1.2 攔截）。"""
from __future__ import annotations

import asyncio
import os
from typing import Any

import reflex as rx

import db_service
from fox_quiz.nav_bar import app_navbar
from fox_quiz.session_state import SessionState

_BG = "linear-gradient(180deg, #f8fafc 0%, #e0f2fe 100%)"
_PLACEHOLDER_IMG = "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=800&auto=format&fit=crop"
_STORAGE_PUBLIC_BASE = f"{(os.getenv('SUPABASE_URL') or '').strip().rstrip('/')}/storage/v1/object/public"


class MatchWallState(rx.State):
    matches: list[dict[str, Any]] = []
    blocked_count: int = 0
    loading: bool = False
    error_msg: str = ""
    unlock_dialog_open: bool = False
    unlock_target_id: str = ""
    unlock_dim_label: str = ""
    unlock_msg: str = ""

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
            for i, r in enumerate(rows):
                path = str(r.get("image_object_path") or "").strip()
                bucket = str(r.get("image_bucket") or "stories").strip() or "stories"
                image_url = (
                    f"{_STORAGE_PUBLIC_BASE}/{bucket}/{path}"
                    if _STORAGE_PUBLIC_BASE and path
                    else _PLACEHOLDER_IMG
                )
                nr = dict(r)
                nr["matched_user_id"] = str(r.get("user_id") or "")
                nr["conflict_dim_label"] = str(r.get("conflict_dim_label") or "待擴充")
                nr["image_url"] = image_url
                nr["card_idx"] = i
                out.append(nr)
            blocked = 0
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

    @rx.event
    def close_unlock_dialog(self) -> None:
        self.unlock_dialog_open = False
        self.unlock_msg = ""

    @rx.event
    def open_unlock_dialog(self, card_idx: int | list[int]) -> None:
        idx = int(card_idx[0]) if isinstance(card_idx, (list, tuple)) and card_idx else int(card_idx)
        if idx < 0 or idx >= len(self.matches):
            return
        row = self.matches[idx]
        if not row.get("is_blurred"):
            return
        self.unlock_dialog_open = True
        self.unlock_target_id = str(row.get("matched_user_id") or "")
        self.unlock_dim_label = str(row.get("conflict_dim_label") or "")
        self.unlock_msg = ""

    @rx.event
    async def submit_unlock_request(self) -> Any:
        sess = await self.get_state(SessionState)
        token = (sess.access_token or "").strip()
        tid = self.unlock_target_id

        def _do():
            db_service.create_unlock(token, tid)

        try:
            await asyncio.to_thread(_do)
            async with self:
                self.unlock_msg = "解鎖請求已送出（Task 9）。"
        except Exception as e:
            async with self:
                self.unlock_msg = f"解鎖失敗：{e}"
            return rx.window_alert(str(e))


def _match_card(item: dict[str, Any]) -> rx.Component:
    is_blurred = item["is_blurred"]
    distance = item["distance"]
    dim_label = item["conflict_dim_label"]
    image_url = item["image_url"]
    card_idx = item["card_idx"]

    inner = rx.vstack(
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
                rx.hstack(
                    rx.text("距離 ", size="2", as_="span"),
                    rx.text(distance, size="2", as_="span"),
                    spacing="1",
                    align_items="center",
                ),
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
            rx.hstack(
                rx.text("預警維度：", size="2", color="red", as_="span"),
                rx.text(dim_label, size="2", color="red", as_="span"),
            ),
            rx.hstack(
                rx.text("主要落差：", size="2", color="gray", as_="span"),
                rx.text(dim_label, size="2", color="gray", as_="span"),
            ),
        ),
        rx.cond(
            is_blurred,
            rx.text(
                "點擊卡片以查看解鎖選項（Task 9）",
                size="1",
                color="gray",
                as_="span",
                display="block",
            ),
            rx.button(
                "詳情（Task 8）",
                variant="outline",
                size="2",
                width="100%",
                disabled=True,
            ),
        ),
        spacing="3",
        width="100%",
        align_items="start",
    )

    return rx.box(
        rx.cond(
            is_blurred,
            rx.box(
                inner,
                width="100%",
                cursor="pointer",
                on_click=MatchWallState.open_unlock_dialog(card_idx),
            ),
            rx.box(inner, width="100%"),
        ),
        width="100%",
    )


def _unlock_overlay() -> rx.Component:
    return rx.cond(
        MatchWallState.unlock_dialog_open,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.heading("模糊對象", size="4"),
                    rx.text(
                        "此檔案經系統模糊處理；解鎖後可於 Task 8 查看清晰內容與攻略。",
                        size="2",
                        color="gray",
                        as_="span",
                        display="block",
                    ),
                    rx.hstack(
                        rx.text("衝突維度：", size="2", weight="bold", as_="span"),
                        rx.text(MatchWallState.unlock_dim_label, size="2", weight="bold", as_="span"),
                    ),
                    rx.text(
                        MatchWallState.unlock_msg,
                        size="2",
                        color="orange",
                        as_="span",
                        display="block",
                    ),
                    rx.hstack(
                        rx.button(
                            "取消",
                            variant="outline",
                            on_click=MatchWallState.close_unlock_dialog,
                        ),
                        rx.button(
                            "解鎖（100 coins）",
                            color_scheme="orange",
                            on_click=MatchWallState.submit_unlock_request,
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="6",
                background="white",
                border_radius="12px",
                max_width="28rem",
                width="100%",
                box_shadow="lg",
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background="rgba(0,0,0,0.45)",
            display="flex",
            align_items="center",
            justify_content="center",
            z_index="9999",
            padding="4",
        ),
        rx.fragment(),
    )


def match_wall_page() -> rx.Component:
    return rx.box(
        rx.fragment(
            rx.vstack(
            app_navbar(),
            rx.heading("北極狐配對牆", size="6", weight="bold"),
            rx.card(
                rx.text(
                    f"守護中：已為您成功攔截 {MatchWallState.blocked_count} 個高風險地雷。",
                    size="3",
                    weight="bold",
                    as_="span",
                    display="block",
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
                    as_="span",
                    display="block",
                ),
            ),
            spacing="4",
            width="100%",
            max_width="52rem",
            padding="6",
            ),
            _unlock_overlay(),
        ),
        min_height="100vh",
        width="100%",
        background=_BG,
    )
