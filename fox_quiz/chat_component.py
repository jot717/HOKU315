"""
Reflex 對話室：織光暖色調、依 dominant 譜系切換狐狸頭像，送出時走 LLMGateway.build_chat_messages。
"""
from __future__ import annotations

import asyncio

import reflex as rx

import db_service
import fox_logic
from fox_quiz.session_state import SessionState
from fox_logic import VECTOR_DIM, dominant_fox_archetype_key, generate_vector
from llm_gateway import LLMGateway

_SAND_BG = "linear-gradient(180deg, #fff9f0 0%, #ffe8cc 55%, #ffd9a8 100%)"
_USER_BUBBLE = "#f2a54a"
_USER_TEXT = "#3d2910"
_FOX_BUBBLE = "#fff4e0"
_FOX_BORDER = "#d4a03a"
_MUTED = "#a65d1a"


def _default_query_vector() -> list[float]:
    return generate_vector([0.5] * VECTOR_DIM)


class ChatState(rx.State):
    """對話列表、RAG 提示與用於檢索／譜系的 query 向量（優先 profile，否則中性預設）。"""

    messages: list[dict[str, str]] = []
    draft: str = ""
    rag_hint: bool = False
    query_vector: list[float] = _default_query_vector()

    @rx.event
    def set_draft(self, value: str | list[str]) -> None:
        if isinstance(value, (list, tuple)) and value:
            self.draft = str(value[0])
        else:
            self.draft = str(value)

    @rx.var(cache=True)
    def archetype_key(self) -> str:
        if len(self.query_vector) != VECTOR_DIM:
            return "weave"
        return dominant_fox_archetype_key(self.query_vector)

    @rx.event(background=True)
    async def load_profile_vector(self):
        sess = await self.get_state(SessionState)
        uid = db_service.resolve_user_id(access_token=sess.access_token)
        if not uid:
            return
        try:
            vec = await asyncio.to_thread(db_service.get_user_vector, uid)
            async with self:
                self.query_vector = vec
        except BaseException:
            pass

    @rx.event(background=True)
    async def send_chat(self):
        async with self:
            text = (self.draft or "").strip()
            if not text:
                return
            self.messages = [*self.messages, {"role": "user", "content": text}]
            self.draft = ""
            self.rag_hint = True
            qv = list(self.query_vector)

        sess = await self.get_state(SessionState)
        uid = db_service.resolve_user_id(access_token=sess.access_token)
        if not uid:
            async with self:
                self.rag_hint = False
                self.messages = [
                    *self.messages,
                    {
                        "role": "assistant",
                        "content": "【系統】請先於「我的故事」頁貼上 access_token，或設定 MOCK_LOGIN_USER_ID／DB_TEST_PROFILE_ID。",
                    },
                ]
            return
        try:
            qv = await asyncio.to_thread(db_service.get_user_vector, uid)
        except BaseException:
            pass

        gw = LLMGateway()
        msgs = await asyncio.to_thread(
            gw.build_chat_messages,
            uid,
            text,
            query_vector=qv,
        )
        system_block = str(msgs[0].get("content", ""))
        ack = await asyncio.to_thread(LLMGateway.simulate_fox_ack, system_block, text)

        async with self:
            self.query_vector = qv
            self.rag_hint = False
            self.messages = [*self.messages, {"role": "assistant", "content": ack}]


def _message_row(msg: rx.Var[dict[str, str]]) -> rx.Component:
    user_bubble = rx.hstack(
        rx.spacer(),
        rx.box(
            msg["content"],
            padding="12px 16px",
            border_radius="18px 18px 4px 18px",
            background=_USER_BUBBLE,
            color=_USER_TEXT,
            max_width="78%",
            font_weight="500",
            box_shadow="0 1px 4px rgba(212, 120, 40, 0.25)",
        ),
        width="100%",
        align="end",
        padding_y="2",
    )
    fox_avatar = rx.box(
        rx.text("🦊", style={"font_size": "1.75rem", "line_height": "1"}),
        width="3rem",
        height="3rem",
        border_radius="50%",
        display="flex",
        align_items="center",
        justify_content="center",
        border="3px solid",
        border_color=rx.cond(
            ChatState.archetype_key == "weave",
            "#e8a838",
            rx.cond(
                ChatState.archetype_key == "vein",
                "#c97c5d",
                rx.cond(
                    ChatState.archetype_key == "rime",
                    "#b8a078",
                    rx.cond(ChatState.archetype_key == "ember", "#e8683c", "#e8a838"),
                ),
            ),
        ),
        background="#fffaf2",
        flex_shrink="0",
    )
    fox_bubble = rx.box(
        msg["content"],
        padding="12px 16px",
        border_radius="18px 18px 18px 4px",
        background=_FOX_BUBBLE,
        color=_USER_TEXT,
        border=f"1px solid {_FOX_BORDER}",
        max_width="78%",
        box_shadow="0 1px 3px rgba(180, 120, 40, 0.12)",
    )
    assistant_row = rx.hstack(
        fox_avatar,
        fox_bubble,
        width="100%",
        align="start",
        spacing="3",
        padding_y="2",
    )
    return rx.cond(msg["role"] == "user", user_bubble, assistant_row)


def chat_page() -> rx.Component:
    return rx.box(
        rx.box(on_mount=ChatState.load_profile_vector, display="none"),
        rx.vstack(
            rx.hstack(
                rx.link(
                    "← 回到測驗",
                    href="/",
                    color=_MUTED,
                    font_weight="medium",
                    _hover={"color": _USER_TEXT},
                ),
                rx.spacer(),
                rx.text(
                    "織光譜系 · 沙漠耳廓狐對話室",
                    size="2",
                    color=_MUTED,
                    weight="medium",
                ),
                width="100%",
                align="center",
                padding_x="4",
                padding_top="4",
            ),
            rx.vstack(
                rx.foreach(ChatState.messages, _message_row),
                rx.cond(
                    ChatState.rag_hint,
                    rx.box(
                        rx.text(
                            "正在回溯你的地雷區記憶...",
                            size="1",
                            color=_MUTED,
                            font_style="italic",
                            padding_left="4rem",
                        ),
                        width="100%",
                        padding_y="2",
                    ),
                    rx.box(),
                ),
                spacing="1",
                width="100%",
                max_height="calc(100vh - 12rem)",
                overflow_y="auto",
                padding_x="4",
                padding_y="3",
            ),
            rx.spacer(),
            rx.divider(color_scheme="orange"),
            rx.hstack(
                rx.input(
                    placeholder="輸入訊息…",
                    value=ChatState.draft,
                    on_change=ChatState.set_draft,
                    flex="1",
                    size="3",
                    variant="surface",
                    color_scheme="orange",
                ),
                rx.button(
                    "送出",
                    on_click=ChatState.send_chat,
                    size="3",
                    color_scheme="orange",
                ),
                width="100%",
                spacing="3",
                padding_x="4",
                padding_y="4",
                align="center",
            ),
            spacing="0",
            width="100%",
            min_height="100vh",
        ),
        width="100%",
        min_height="100vh",
        background=_SAND_BG,
    )
