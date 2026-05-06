"""
狐狸性向測驗：20 題社交地雷維度，每題以滑桿 0–1 表示敏感程度。
"""
from __future__ import annotations

import asyncio

import reflex as rx

import db_service
from fox_quiz.chat_component import chat_page
from fox_quiz.login_page import login_page
from fox_quiz.match_wall import MatchWallState, match_wall_page
from fox_quiz.nav_bar import app_navbar
from fox_quiz.session_state import SessionState
from fox_quiz.story_page import story_page
from fox_quiz.unlocks_page import unlocks_page
from fox_logic import (
    SOCIAL_MINE_DIMENSIONS,
    VECTOR_DIM,
    dominant_fox_message,
    generate_vector,
)


def _format_sync_error(exc: BaseException) -> str:
    """擷取 PostgREST / Supabase 錯誤碼與訊息，供 UI 顯示。"""
    try:
        from postgrest.exceptions import APIError

        if isinstance(exc, APIError):
            payload = exc.args[0] if exc.args else {}
            if isinstance(payload, dict):
                code = payload.get("code", "")
                msg = payload.get("message", str(exc))
                return f"{msg} (code={code})" if code else str(msg)
    except ImportError:
        pass
    return str(exc)


class QuizState(rx.State):
    """20 維滑桿分數，順序與 fox_logic.SOCIAL_MINE_DIMENSIONS 一致。"""

    scores: list[float] = [0.5] * VECTOR_DIM
    result_preview: str = ""
    result_is_error: bool = False

    @rx.var(cache=True)
    def score_labels(self) -> list[str]:
        """與 scores 同步的兩位小數標籤，供每題徽章顯示。"""
        v = generate_vector(self.scores)
        return [f"{x:.2f}" for x in v]

    @rx.var(cache=True)
    def live_vector_digest(self) -> str:
        """scores 變動時自動重算的即時向量摘要（經 generate_vector）。"""
        v = generate_vector(self.scores)
        mean_all = sum(v) / float(len(v))
        return (
            f"即時向量預覽：全維均值 {mean_all:.2f} · "
            f"首三維 {v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f} · 末維 {v[-1]:.2f}"
        )

    @staticmethod
    def _coerce_slider_value(value: list[float | int] | float | int) -> float:
        if isinstance(value, (list, tuple)):
            if not value:
                return 0.5
            return float(value[0])
        return float(value)

    @rx.event
    def set_score_at(self, index: int, value: list[float | int] | float | int) -> None:
        """on_change 即時寫回 scores；整表替換以觸發依賴 scores 的 @rx.var 重算。"""
        v = self._coerce_slider_value(value)
        if v < 0.0:
            v = 0.0
        elif v > 1.0:
            v = 1.0
        cur = float(self.scores[index])
        if abs(cur - v) < 1e-6:
            return
        new_s = [*self.scores]
        new_s[index] = v
        self.scores = new_s

    @rx.event
    async def generate_result(self):
        """產生結果並將 20 維向量以 UPSERT 寫入 Supabase。"""
        async with self:
            self.result_is_error = False
            snap = list(self.scores)

        vec = generate_vector(snap)
        fox = dominant_fox_message(vec)
        head = ", ".join(f"{x:.3f}" for x in vec[:5])
        tech = f"（技術摘要）前 5 維：{head} … 共 {len(vec)} 維"

        sess = await self.get_state(SessionState)
        token = (sess.access_token or "").strip()
        user_id = db_service.resolve_user_id(access_token=token)
        if not user_id:
            async with self:
                self.result_is_error = True
                self.result_preview = (
                    f"{fox}\n\n[未登入] 請先至「登入」頁以 Email／密碼登入，"
                    f"或於環境設定 MOCK_LOGIN_USER_ID／DB_TEST_PROFILE_ID（遷移期）。\n\n{tech}"
                )
            return

        try:
            await asyncio.to_thread(db_service.ensure_user_profile, token)
            await asyncio.to_thread(db_service.upsert_user_vector, token, vec)
        except BaseException as e:
            err = _format_sync_error(e)
            async with self:
                self.result_is_error = True
                self.result_preview = f"{fox}\n\n[同步失敗] {err}\n\n{tech}"
            return

        cloud = "☁️ 數據已同步至雲端脈絡"
        async with self:
            self.result_is_error = False
            self.result_preview = f"{fox}\n\n{cloud}\n\n{tech}"

    @rx.event
    async def submit_quiz(self):
        """相容舊事件名：委派至 generate_result。"""
        return await self.generate_result()


def _question_card(index: int, label: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(f"{index + 1} / {VECTOR_DIM}", variant="soft", color="gray"),
                rx.text(label, weight="bold", size="3"),
                align="center",
                spacing="3",
                width="100%",
            ),
            rx.hstack(
                rx.slider(
                    min=0,
                    max=1,
                    step=0.01,
                    value=[QuizState.scores[index]],
                    on_change=QuizState.set_score_at(index).throttle(24),
                    width="100%",
                    flex="1",
                    size="2",
                    color_scheme="orange",
                    high_contrast=True,
                    variant="surface",
                ),
                rx.badge(
                    QuizState.score_labels[index],
                    variant="surface",
                    color_scheme="orange",
                    size="2",
                    min_width="3.5rem",
                    align="center",
                ),
                width="100%",
                align="center",
                spacing="3",
            ),
            rx.hstack(
                rx.text("0 地雷感低", size="1", color="gray"),
                rx.spacer(),
                rx.text("1 地雷感高", size="1", color="gray"),
                width="100%",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
    )


class RootRedirectState(rx.State):
    @rx.event
    async def go_match(self):
        return rx.redirect("/match")


def splash_home() -> rx.Component:
    return rx.center(rx.spinner(), min_height="100vh", width="100%")


def quiz_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            app_navbar(),
            rx.heading("狐狸性向測驗", size="7", weight="bold"),
            rx.text(
                "共 20 題。拖曳滑桿：越靠右代表你在該情境越容易「踩雷」或感到壓力。",
                color="gray",
                size="2",
            ),
            rx.text(
                QuizState.live_vector_digest,
                size="1",
                color="gray",
                width="100%",
            ),
            rx.divider(margin_y="4"),
            rx.vstack(
                *[
                    _question_card(i, label)
                    for i, (_, label) in enumerate(SOCIAL_MINE_DIMENSIONS)
                ],
                spacing="4",
                width="100%",
            ),
            rx.divider(margin_y="4"),
            rx.hstack(
                rx.button(
                    "產生結果向量",
                    on_click=QuizState.generate_result,
                    size="3",
                    color_scheme="orange",
                ),
                width="100%",
            ),
            rx.cond(
                QuizState.result_preview != "",
                rx.cond(
                    QuizState.result_is_error,
                    rx.callout(
                        rx.text(
                            QuizState.result_preview,
                            white_space="pre-wrap",
                            width="100%",
                            size="2",
                        ),
                        icon="triangle-alert",
                        color="red",
                        margin_top="4",
                        width="100%",
                    ),
                    rx.callout(
                        rx.text(
                            QuizState.result_preview,
                            white_space="pre-wrap",
                            width="100%",
                            size="2",
                        ),
                        icon="check",
                        color="green",
                        margin_top="4",
                        width="100%",
                    ),
                ),
                rx.box(),
            ),
            spacing="4",
            width="100%",
            max_width="48rem",
            padding_bottom="8",
            padding_x="6",
            padding_y="8",
        ),
        min_height="100vh",
        width="100%",
        background="var(--gray-2)",
    )


app = rx.App(theme=rx.theme(appearance="light", accent_color="orange"))
app.add_page(splash_home, route="/", title="JOT717", on_load=RootRedirectState.go_match)
app.add_page(quiz_page, route="/quiz", title="狐狸性向測驗")
app.add_page(login_page, route="/login", title="登入")
app.add_page(chat_page, route="/chat", title="狐狸對話室")
app.add_page(
    story_page,
    route="/story",
    title="我的故事",
    on_load=SessionState.guard_protected_routes,
)
app.add_page(
    match_wall_page,
    route="/match",
    title="配對牆",
    on_load=MatchWallState.load_match_wall,
)
app.add_page(
    unlocks_page,
    route="/unlocks",
    title="解鎖",
    on_load=SessionState.guard_protected_routes,
)
