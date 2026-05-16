"""裝置端 Session：認證欄位持久化於 LocalStorage（Phase2 帳號／備份；實作細節見 docs/deprecated/future_sns_layer）。"""
from __future__ import annotations

from typing import Any

import reflex as rx

import db_service


class SessionState(rx.State):
    access_token: str = rx.LocalStorage("", name="hok315_supabase_access", sync=True)
    refresh_token: str = rx.LocalStorage("", name="hok315_supabase_refresh", sync=True)

    @rx.event
    def set_access_token(self, value: str | list[str]) -> None:
        if isinstance(value, (list, tuple)) and value:
            self.access_token = str(value[0]).strip()
        else:
            self.access_token = str(value or "").strip()

    @rx.event
    def sign_out(self) -> Any:
        self.access_token = ""
        self.refresh_token = ""
        return rx.redirect("/login")

    @rx.event
    async def guard_protected_routes(self) -> Any:
        """未登入或登入失效時導向 /login（供 /story、/match on_load）。"""
        t = (self.access_token or "").strip()
        if not t:
            return rx.redirect("/login")
        uid = db_service.user_id_from_access_token(t)
        if not uid:
            self.access_token = ""
            self.refresh_token = ""
            return rx.redirect("/login")
        return
