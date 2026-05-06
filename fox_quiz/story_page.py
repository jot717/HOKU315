"""
個人故事：拖放圖片 → **先上傳 Supabase Storage**，成功後再寫入 `stories`。
"""
from __future__ import annotations

import asyncio
import base64
import os
from pathlib import Path
from typing import Any

import reflex as rx
from reflex import UploadFile

import db_service
from fox_quiz.nav_bar import app_navbar
from fox_quiz.session_state import SessionState

_BG = "linear-gradient(180deg, #fff9f0 0%, #ffe8cc 100%)"


def _guess_content_type(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }.get(ext, "application/octet-stream")


class StoryState(rx.State):
    title: str = ""
    body: str = ""
    image_basename: str = "story_cover.jpg"
    status_msg: str = ""
    upload_hint: str = "尚未選檔（拖放後將先上傳 Storage）"
    pending_image_b64: str = ""
    uploading: bool = False

    @rx.event
    def set_title(self, value: str | list[str]) -> None:
        self.title = str(value[0] if isinstance(value, (list, tuple)) and value else value or "")

    @rx.event
    def set_body(self, value: str | list[str]) -> None:
        self.body = str(value[0] if isinstance(value, (list, tuple)) and value else value or "")

    @rx.event
    def set_image_basename(self, value: str | list[str]) -> None:
        self.image_basename = str(value[0] if isinstance(value, (list, tuple)) and value else value or "").strip() or "story_cover.jpg"

    @rx.event
    async def on_image_drop(self, files: list[UploadFile]):
        if not files:
            return
        uf = files[0]
        name = uf.name or uf.filename or "upload.png"
        raw: bytes
        try:
            raw = await uf.read()
        except Exception:
            fobj = getattr(uf, "file", None)
            if fobj is not None:
                try:
                    fobj.seek(0)
                    raw = fobj.read()
                except Exception:
                    raw = b""
            else:
                raw = b""
        if not raw:
            async with self:
                self.upload_hint = "讀取檔案失敗，請重試"
            return
        b64 = base64.b64encode(raw).decode("ascii")
        bn = Path(name).name
        async with self:
            self.image_basename = name
            self.pending_image_b64 = b64
            self.upload_hint = f"已選檔：{bn}（將上傳至 bucket stories，路徑：<你的UUID>/{bn}）"

    @rx.event
    async def submit_story(self) -> Any:
        async with self:
            self.uploading = True
            self.status_msg = "上傳中…"

        sess = await self.get_state(SessionState)
        token = (sess.access_token or "").strip()

        async with self:
            title = self.title.strip()
            body = self.body.strip()
            img = self.image_basename.strip() or "story_cover.jpg"
            b64 = self.pending_image_b64.strip()

        if not token:
            async with self:
                self.uploading = False
                self.status_msg = "尚未登入：請至「登入」頁使用 Email／密碼。"
            return rx.window_alert("尚未登入：請至「登入」頁使用 Email／密碼。")

        uid = db_service.user_id_from_access_token(token)
        if not uid:
            async with self:
                self.uploading = False
                self.status_msg = "登入狀態失效，請重新登入。"
            return rx.window_alert("登入狀態失效，請重新登入。")

        if not b64:
            async with self:
                self.uploading = False
                self.status_msg = "請先拖放圖片：會先上傳 Storage（user_id/檔名），成功後才寫入資料庫。"
            return rx.window_alert("請先拖放圖片後再儲存。")

        try:
            raw = base64.b64decode(b64.encode("ascii"))
        except Exception:
            async with self:
                self.uploading = False
                self.status_msg = "圖片資料無效，請重新選檔。"
            return rx.window_alert("圖片資料無效，請重新選檔。")

        def _preflight_profile():
            db_service.ensure_user_profile(token)

        try:
            await asyncio.to_thread(_preflight_profile)
        except Exception as e:
            async with self:
                self.uploading = False
                self.status_msg = f"無法同步 profiles（RLS 42501？請執行 sql/profiles_rls.sql）：{e}"
            return rx.window_alert(f"無法同步 profiles：{e}")

        path = db_service.story_image_object_path(uid, img)
        ctype = _guess_content_type(img)

        def _upload():
            return db_service.upload_to_supabase_storage(
                token,
                path,
                raw,
                content_type=ctype if ctype != "application/octet-stream" else "image/png",
            )

        try:
            await asyncio.to_thread(_upload)
        except Exception as e:
            async with self:
                self.uploading = False
                self.status_msg = f"Storage 上傳失敗（請確認已執行 sql/stories.sql、bucket stories、RLS）：{e}"
            return rx.window_alert(f"Storage 上傳失敗：{e}")

        def _insert():
            db_service.ensure_user_profile(token)
            return db_service.create_story(
                access_token=token,
                title=title or None,
                body=body or None,
                image_object_path=path,
            )

        try:
            await asyncio.to_thread(_insert)
            rows = await asyncio.to_thread(db_service.get_user_stories, token)
            supabase_url = (os.getenv("SUPABASE_URL") or "").strip().rstrip("/")
            public_url = f"{supabase_url}/storage/v1/object/public/stories/{path}" if supabase_url else path
            print(f"DEBUG_URL: {public_url}")
            async with self:
                self.uploading = False
                self.pending_image_b64 = ""
                self.status_msg = (
                    f"已完成：Storage `{path}` → DB 紀錄（共 {len(rows)} 筆故事）。"
                )
        except Exception as e:
            async with self:
                self.uploading = False
                self.status_msg = f"資料庫寫入失敗（檔案可能已在 Storage）：{e}"
            return rx.window_alert(f"資料庫寫入失敗（檔案可能已在 Storage）：{e}")


def story_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            app_navbar(),
            rx.heading("我的故事（Story）", size="6", weight="bold"),
            rx.text(
                "登入後 Session 會自動帶入 JWT。拖放圖片時系統會 **先上傳至 bucket「stories」**（路徑 "
                "`{你的 user_id}/{檔名}`），成功後才寫入 `stories` 表。需已在 Supabase 執行 "
                "`sql/stories.sql`（含 Storage RLS）。",
                size="2",
                color="gray",
            ),
            rx.card(
                rx.vstack(
                    rx.input(
                        placeholder="標題",
                        value=StoryState.title,
                        on_change=StoryState.set_title,
                        width="100%",
                    ),
                    rx.text_area(
                        placeholder="故事內文",
                        value=StoryState.body,
                        on_change=StoryState.set_body,
                        min_height="120px",
                        width="100%",
                    ),
                    rx.text("圖片（拖放或點擊）— 必填", size="2", weight="bold"),
                    rx.upload(
                        rx.vstack(
                            rx.icon("image", size=32, color="orange"),
                            rx.text(StoryState.upload_hint, size="1", color="gray"),
                        ),
                        id="story_image_upload",
                        border="1px dashed #e8a838",
                        padding="2rem",
                        multiple=False,
                        accept={"image/*": [".png", ".jpg", ".jpeg", ".gif", ".webp"]},
                        on_drop=StoryState.on_image_drop,
                        width="100%",
                    ),
                    rx.hstack(
                        rx.text("或手動檔名", size="1", color="gray"),
                        rx.input(
                            value=StoryState.image_basename,
                            on_change=StoryState.set_image_basename,
                            flex="1",
                        ),
                        width="100%",
                        align="center",
                    ),
                    rx.button(
                        rx.cond(
                            StoryState.uploading,
                            "上傳中…",
                            "上傳圖片並儲存故事",
                        ),
                        on_click=StoryState.submit_story,
                        color_scheme="orange",
                        size="3",
                        disabled=StoryState.uploading,
                    ),
                    rx.text(StoryState.status_msg, size="2", color="gray", white_space="pre-wrap"),
                    spacing="3",
                    width="100%",
                ),
                width="100%",
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
