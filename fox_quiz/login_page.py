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
        except Exception as e:
            async with self:
                self.message = f"登入失敗：{e}"
            return

        token = data["access_token"]

        def _ensure_profile():
            db_service.ensure_user_profile(token)

        try:
            await asyncio.to_thread(_ensure_profile)
        except Exception as e:
            async with self:
                self.message = f"無法同步 profiles（請確認 RLS 允許使用者建立自己的列）：{e}"
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
        return rx.redirect("/match" if has_custom else "/story")

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
        except Exception as e:
            async with self:
                self.message = f"註冊失敗：{e}"
            return

        token = data["access_token"]

        def _ensure_profile():
            db_service.ensure_user_profile(token)

        try:
            await asyncio.to_thread(_ensure_profile)
        except Exception as e:
            async with self:
                self.message = f"無法建立 profiles（請確認 RLS／表結構）：{e}"
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
        return rx.redirect("/match" if has_custom else "/story")


def login_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("登入 JOT717", size="6", weight="bold"),
            rx.text("使用 Supabase Auth（Email／密碼），成功後 token 存於裝置，不必手動貼上。", size="2", color="gray"),
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
                    rx.text(LoginState.message, size="2", color="red", white_space="pre-wrap"),
                    width="100%",
                    spacing="3",
                ),
                width="100%",
            ),
            rx.hstack(
                rx.link("← 配對牆", href="/match", color="orange", size="2"),
                rx.link("測驗", href="/quiz", color="gray", size="2"),
                spacing="4",
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
