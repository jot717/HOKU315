"""Email／密碼登入與註冊；成功後寫入 SessionState（LocalStorage 持久化）。"""
from __future__ import annotations

import asyncio
from typing import Any

import reflex as rx

import db_service
from fox_quiz.session_state import SessionState

_BG = "linear-gradient(180deg, #f8fafc 0%, #ffedd5 100%)"


class LoginState(rx.State):
    email: str = ""
    password: str = ""
    message: str = ""

    @rx.event
    def set_email(self, value: str | list[str]) -> None:
        self.email = str(value[0] if isinstance(value, (list, tuple)) and value else value or "")

    @rx.event
    def set_password(self, value: str | list[str]) -> None:
        self.password = str(value[0] if isinstance(value, (list, tuple)) and value else value or "")

    @rx.event
    async def submit_login(self) -> Any:
        async with self:
            email = self.email.strip()
            password = self.password
            self.message = ""
        if not email or not password:
            async with self:
                self.message = "請輸入 email 與密碼。"
            return

        def _do():
            return db_service.auth_sign_in_email_password(email, password)

        try:
            data = await asyncio.to_thread(_do)
        except Exception:
            async with self:
                self.message = "登入未完成，請確認帳號密碼與網路後再試。"
            return

        token = data["access_token"]

        def _ensure_profile():
            db_service.ensure_user_profile(token)

        try:
            await asyncio.to_thread(_ensure_profile)
        except Exception as e:
            async with self:
                self.message = "無法完成帳號準備，請稍後再試或檢查網路與權限設定。"
            return

        sess = await self.get_state(SessionState)
        async with sess:
            sess.access_token = token
            sess.refresh_token = data.get("refresh_token", "")

        def _route() -> bool:
            return db_service.profile_has_custom_vector(token)

        try:
            has_custom = await asyncio.to_thread(_route)
        except Exception:
            has_custom = False
        return rx.redirect("/match" if has_custom else "/profile")

    @rx.event
    async def submit_signup(self) -> Any:
        async with self:
            email = self.email.strip()
            password = self.password
            self.message = ""
        if not email or not password:
            async with self:
                self.message = "請輸入 email 與密碼。"
            return

        def _do():
            return db_service.auth_sign_up_email_password(email, password)

        try:
            data = await asyncio.to_thread(_do)
        except LookupError as e:
            async with self:
                self.message = str(e)
            return
        except Exception:
            async with self:
                self.message = "註冊未完成，請稍後再試。"
            return

        token = data["access_token"]

        def _ensure_profile():
            db_service.ensure_user_profile(token)

        try:
            await asyncio.to_thread(_ensure_profile)
        except Exception as e:
            async with self:
                self.message = "無法完成註冊後的帳號準備，請稍後再試或檢查權限設定。"
            return

        sess = await self.get_state(SessionState)
        async with sess:
            sess.access_token = token
            sess.refresh_token = data.get("refresh_token", "")

        def _route() -> bool:
            return db_service.profile_has_custom_vector(token)

        try:
            has_custom = await asyncio.to_thread(_route)
        except Exception:
            has_custom = False
        return rx.redirect("/match" if has_custom else "/profile")


def login_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("帳號登入", size="6", weight="bold"),
            rx.text(
                "帳號模式可保存問卷向量、配對牆與長期互動趨勢。"
                "若只想先體驗分析，無需登入。",
                size="2",
                color="gray",
                as_="span",
                display="block",
            ),
            rx.card(
                rx.vstack(
                    rx.text("訪客模式", size="2", weight="bold", as_="span"),
                    rx.text(
                        "在本機完成訊號檔案、問卷、觀察對象與互動分析；"
                        "不保證跨裝置同步。",
                        size="2",
                        color="gray",
                        as_="span",
                        style={"line_height": "1.55"},
                    ),
                    rx.link(
                        rx.button("返回首頁 · 立即開始分析", variant="soft", width="100%", size="2"),
                        href="/",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                width="100%",
                margin_bottom="4",
            ),
            rx.card(
                rx.vstack(
                    rx.input(
                        placeholder="email@example.com",
                        value=LoginState.email,
                        on_change=LoginState.set_email,
                        type="email",
                        width="100%",
                    ),
                    rx.input(
                        placeholder="密碼",
                        value=LoginState.password,
                        on_change=LoginState.set_password,
                        type="password",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button("登入", on_click=LoginState.submit_login, color_scheme="orange", size="3"),
                        rx.button("註冊", on_click=LoginState.submit_signup, variant="outline", size="3"),
                        spacing="3",
                    ),
                    rx.text(
                        LoginState.message,
                        size="2",
                        color="red",
                        white_space="pre-wrap",
                        as_="span",
                        display="block",
                        width="100%",
                    ),
                    width="100%",
                    spacing="3",
                ),
                width="100%",
            ),
            rx.hstack(
                rx.link("← 首頁", href="/", color="gray", size="2"),
                rx.link("訊號問卷", href="/quiz", color="gray", size="2"),
                rx.link("分析結果", href="/insight", color="orange", size="2"),
                spacing="4",
                flex_wrap="wrap",
            ),
            spacing="4",
            max_width="24rem",
            width="100%",
            padding="8",
        ),
        min_height="100vh",
        width="100%",
        display="flex",
        align_items="center",
        justify_content="center",
        background=_BG,
    )
