"""Task 7：北極狐訊號牆（UAT-04 門檻：0.7 模糊、1.2 攔截）。"""
from __future__ import annotations

import asyncio
import os
from typing import Any

import reflex as rx

import db_service
from fox_quiz.nav_bar import app_navbar
from fox_quiz.session_state import SessionState
from product.profile.runtime.profile_store import load_profile
from product.signal.runtime.signal_inference_engine import (
    collect_signal_profile_for_inference,
    infer_signal_risks,
)
from product.match.runtime.match_rhythm_engine import generate_match_credibility_bundle

_BG = "linear-gradient(180deg, #f8fafc 0%, #e0f2fe 100%)"
_PLACEHOLDER_IMG = "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=800&auto=format&fit=crop"
_STORAGE_PUBLIC_BASE = f"{(os.getenv('SUPABASE_URL') or '').strip().rstrip('/')}/storage/v1/object/public"


def _coerce_distance(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 1.0


def _local_user_inference() -> dict[str, Any]:
    bundle = collect_signal_profile_for_inference(None, None)
    return infer_signal_risks(bundle)


def enrich_match_row_for_ui(
    row: dict[str, Any],
    card_idx: int,
    *,
    inference: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Precompute tiers + UX social causality in plain Python — never compare floats inside rx.foreach."""
    nr = dict(row)
    d = _coerce_distance(nr.get("distance"))
    blurred = bool(nr.get("is_blurred"))

    if d <= 0.35:
        compat_bucket = "h"
    elif d < 0.7:
        compat_bucket = "m"
    else:
        compat_bucket = "l"
    nr["compat_bucket"] = compat_bucket

    if blurred:
        risk_bucket = "h"
    elif d < 0.45:
        risk_bucket = "l"
    else:
        risk_bucket = "m"
    nr["risk_bucket"] = risk_bucket

    inf = inference if inference is not None else _local_user_inference()
    cred = generate_match_credibility_bundle(
        distance=d,
        compat_bucket=compat_bucket,
        conflict_dim_label=str(nr.get("conflict_dim_label") or ""),
        blurred=blurred,
        user_inference=inf,
        profile=load_profile(),
    )
    nr["peer_archetype"] = cred["peer_archetype"]
    nr["interaction_rhythm_line"] = cred["interaction_rhythm_line"]
    nr["reply_pressure_line"] = cred["reply_pressure_line"]
    nr["emotional_pacing_line"] = cred["emotional_pacing_line"]
    nr["energy_safety_line"] = cred["energy_safety_line"]
    nr["exhaustion_point_line"] = cred["exhaustion_point_line"]
    nr["scenario_line"] = cred["scenario_line"]
    nr["energy_badge"] = cred.get("energy_safety", "中等")
    nr["emotion_line"] = cred["interaction_rhythm_line"]
    nr["rhythm_line"] = cred["reply_pressure_line"]
    nr["match_rationale_line"] = cred["energy_safety_line"]
    nr["fatigue_avoided_line"] = cred["exhaustion_point_line"]

    nr["distance_str"] = f"{d:.3f}"
    nr["card_idx"] = card_idx
    return nr


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
            inference = _local_user_inference()
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
                out.append(enrich_match_row_for_ui(nr, i, inference=inference))
            blocked = 0
            return out, blocked

        try:
            rows, blocked = await asyncio.to_thread(_load)
        except Exception as e:
            async with self:
                self.loading = False
                self.matches = []
                self.blocked_count = 0
                self.error_msg = "訊號牆暫時無法載入，請確認網路後重試。"
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
                self.unlock_msg = "解鎖請求已送出。"
        except Exception:
            async with self:
                self.unlock_msg = "解鎖未完成，請稍後再試。"
            return rx.window_alert("解鎖未完成，請稍後再試。")


def _energy_badge(item: dict[str, Any]) -> rx.Component:
    safety = item["energy_badge"]
    return rx.cond(
        safety == "偏高",
        rx.badge("社交電量：較省", color_scheme="green", variant="soft"),
        rx.cond(
            safety == "偏低",
            rx.badge("社交電量：偏耗", color_scheme="red", variant="soft"),
            rx.badge("社交電量：中等", color_scheme="orange", variant="soft"),
        ),
    )


def _risk_badge(item: dict[str, Any]) -> rx.Component:
    r = item["risk_bucket"]
    return rx.cond(
        r == "h",
        rx.badge("風險：高", color_scheme="red", variant="surface"),
        rx.cond(
            r == "l",
            rx.badge("風險：低", color_scheme="green", variant="surface"),
            rx.badge("風險：中", color_scheme="orange", variant="surface"),
        ),
    )


def _match_card(item: dict[str, Any]) -> rx.Component:
    is_blurred = item["is_blurred"]
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
        _energy_badge(item),
        rx.text(
            item["interaction_rhythm_line"],
            size="2",
            color="gray",
            as_="span",
        ),
        rx.text(
            item["reply_pressure_line"],
            size="2",
            color="gray",
            as_="span",
        ),
        rx.text(
            item["emotional_pacing_line"],
            size="2",
            color="gray",
            as_="span",
        ),
        rx.text(
            item["energy_safety_line"],
            size="2",
            color="gray",
            as_="span",
        ),
        rx.text(
            item["exhaustion_point_line"],
            size="2",
            color="gray",
            as_="span",
        ),
        _risk_badge(item),
        rx.vstack(
            rx.text("互動情境", size="1", color="gray", weight="bold", as_="span"),
            rx.text(
                item["scenario_line"],
                size="2",
                color="gray",
                as_="span",
            ),
            rx.hstack(
                rx.text("訊號距離", size="1", color="gray", as_="span"),
                rx.text(item["distance_str"], size="1", weight="medium", as_="span"),
                spacing="2",
            ),
            spacing="1",
            align_items="start",
            width="100%",
        ),
        rx.hstack(
            rx.badge(
                rx.cond(is_blurred, "需留意", "可觀察"),
                color_scheme=rx.cond(is_blurred, "red", "green"),
                variant="soft",
            ),
            width="100%",
        ),
        rx.cond(
            is_blurred,
            rx.text(
                "點擊卡片以查看解鎖選項",
                size="1",
                color="gray",
                as_="span",
                display="block",
            ),
            rx.button(
                "詳情（稍後開放）",
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
                rx.heading("社交電量相容對象", size="6", weight="bold"),
                rx.text(
                    "每張卡片依互動節奏、回覆壓力與社交電量安全度解讀——不是約會分數或性格類型。",
                    size="2",
                    color="gray",
                    as_="span",
                    display="block",
                ),
                rx.card(
                    rx.hstack(
                        rx.text("目前已為你屏蔽 ", size="3", as_="span"),
                        rx.text(MatchWallState.blocked_count, size="3", weight="bold", as_="span"),
                        rx.text(" 筆高落差訊號。", size="3", as_="span"),
                        spacing="1",
                        align_items="center",
                        flex_wrap="wrap",
                    ),
                    width="100%",
                    background="rgba(255, 237, 213, 0.65)",
                ),
                rx.hstack(
                    rx.button(
                        rx.cond(MatchWallState.loading, "載入中…", "重新載入"),
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
