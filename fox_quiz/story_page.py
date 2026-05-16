"""
個人故事：拖放圖片後上傳，再寫入故事紀錄（Phase2 雲端細節見 deprecated 說明）。
"""
from __future__ import annotations

import asyncio
import base64
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
    upload_hint: str = "尚未選檔（拖放圖片後即可儲存）"
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
            self.upload_hint = f"已選檔：{bn}（將隨故事一併儲存）"

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
                self.status_msg = "請先拖放圖片，再按儲存。"
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
                self.status_msg = "無法完成故事上傳前準備，請稍後再試。"
            return rx.window_alert("無法完成故事上傳前準備，請稍後再試。")

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
                self.status_msg = "圖片上傳失敗，請檢查網路後重試。"
            return rx.window_alert("圖片上傳失敗，請檢查網路後重試。")

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
            async with self:
                self.uploading = False
                self.pending_image_b64 = ""
                self.status_msg = f"故事已儲存（共 {len(rows)} 筆）。"
        except Exception as e:
            async with self:
                self.uploading = False
                self.status_msg = "故事寫入未完成，請稍後重試。"
            return rx.window_alert("故事寫入未完成，請稍後重試。")


def story_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            app_navbar(),
            rx.heading("我的故事（Story）", size="6", weight="bold"),
            rx.text(
                "登入後可上傳封面圖並儲存故事；圖片會與故事一併保存。",
                size="2",
                color="gray",
                as_="span",
                display="block",
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
                    rx.text(
                        "圖片（拖放或點擊）— 必填",
                        size="2",
                        weight="bold",
                        as_="span",
                        display="block",
                    ),
                    rx.upload(
                        rx.vstack(
                            rx.icon("image", size=32, color="orange"),
                            rx.text(StoryState.upload_hint, size="1", color="gray", as_="span"),
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
                        rx.text("或手動檔名", size="1", color="gray", as_="span"),
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
                    rx.text(
                        StoryState.status_msg,
                        size="2",
                        color="gray",
                        white_space="pre-wrap",
                        as_="span",
                        display="block",
                    ),
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
