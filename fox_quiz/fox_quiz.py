"""
狐狸性向測驗：20 題社交地雷維度，每題以滑桿 0–1 表示敏感程度。
"""
from __future__ import annotations

import asyncio

import reflex as rx

import db_service
from fox_quiz.login_page import login_page
from fox_quiz.match_wall import MatchWallState, match_wall_page
from fox_quiz.nav_bar import app_navbar
from fox_quiz.session_state import SessionState
from fox_quiz.state.app_state import AppState
from fox_quiz.state.profile_state import ProfileState
from fox_quiz.state.target_state import TargetState
from fox_quiz.ui.app_page import app_page
from fox_quiz.ui.pages.home_page import home_page
from fox_quiz.ui.pages.target_page import target_page
from fox_quiz.ui.profile_page import profile_page
from fox_logic import (
    SOCIAL_MINE_DIMENSIONS,
    VECTOR_DIM,
    dominant_fox_message,
    generate_vector,
)


def _format_sync_error(exc: BaseException) -> str:
    """擷取後端錯誤碼與訊息（除錯／日誌用，不應直接當作 Phase1 主流程文案）。"""
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

    @rx.var(cache=True)
    def score_labels(self) -> list[str]:
        """與 scores 對齊的兩位小數標籤，供每題徽章顯示。"""
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
        """產生訊號結果；優先本機摘要，雲端備份為可選（見 Phase 邊界文件）。"""
        async with self:
            snap = list(self.scores)

        vec = generate_vector(snap)
        fox = dominant_fox_message(vec)
        summary_footer = (
            "\n\n訊號摘要已依問卷更新。接下來可到「觀察對象」與「分析結果」延續同一路徑。"
        )

        sess = await self.get_state(SessionState)
        token = (sess.access_token or "").strip()
        user_id = db_service.resolve_user_id(access_token=token)
        if not user_id:
            async with self:
                self.result_preview = f"{fox}{summary_footer}"
            return

        try:
            await asyncio.to_thread(db_service.ensure_user_profile, token)
            await asyncio.to_thread(db_service.upsert_user_vector, token, vec)
        except BaseException as e:
            _ = _format_sync_error(e)
            async with self:
                self.result_preview = (
                    f"{fox}{summary_footer}\n\n"
                    "（本機摘要已就緒；若之後啟用帳號與備份流程，可再完成一次即可。）"
                )
            return

        async with self:
            self.result_preview = f"{fox}{summary_footer}"

    @rx.event
    async def submit_quiz(self):
        """相容舊事件名：委派至 generate_result。"""
        return await self.generate_result()


def _question_card(index: int, label: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(f"{index + 1} / {VECTOR_DIM}", variant="soft", color="gray"),
                rx.text(label, weight="bold", size="3", as_="span"),
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
                rx.text("0 地雷感低", size="1", color="gray", as_="span"),
                rx.spacer(),
                rx.text("1 地雷感高", size="1", color="gray", as_="span"),
                width="100%",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
    )


def quiz_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            app_navbar(),
            rx.heading("社交訊號問卷", size="7", weight="bold"),
            rx.text(
                "這 20 題會分析你的互動敏感度與危險關係耐受度。",
                size="2",
                color="gray",
                as_="span",
                display="block",
            ),
            rx.box(
                rx.vstack(
                    rx.text(
                        "系統正在分析：",
                        size="2",
                        weight="bold",
                        as_="span",
                    ),
                    rx.text(
                        "- 情緒索取耐受度\n"
                        "- 操控敏感度\n"
                        "- 社交疲勞節奏\n"
                        "- 高壓關係停留傾向\n"
                        "- 衝突逃避模式",
                        size="2",
                        color="gray",
                        style={"line_height": "1.75", "white_space": "pre-wrap"},
                        as_="span",
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                padding="1rem",
                border_radius="12px",
                width="100%",
                border="1px solid rgba(200, 215, 235, 0.65)",
                background="rgba(255,255,255,0.72)",
            ),
            rx.text(
                "共 20 題。拖曳滑桿：越靠右代表你在該情境越容易「踩雷」或感到壓力。",
                color="gray",
                size="2",
                as_="span",
                display="block",
            ),
            rx.text(
                QuizState.live_vector_digest,
                size="1",
                color="gray",
                width="100%",
                as_="span",
                display="block",
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
            rx.text(
                "完成後，系統會開始建立你的危險互動模型。",
                size="2",
                color="gray",
                as_="span",
                display="block",
            ),
            rx.hstack(
                rx.button(
                    "產生結果向量",
                    on_click=QuizState.generate_result,
                    size="3",
                    color_scheme="orange",
                ),
                rx.link(
                    rx.button(
                        "下一步：設定觀察對象",
                        size="3",
                        variant="outline",
                    ),
                    href="/target",
                ),
                spacing="3",
                flex_wrap="wrap",
                width="100%",
            ),
            rx.cond(
                QuizState.result_preview != "",
                rx.callout(
                    QuizState.result_preview,
                    icon="check",
                    color="green",
                    margin_top="4",
                    width="100%",
                    style={"white_space": "pre-wrap"},
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
app.add_page(home_page, route="/", title="HOKU315")
app.add_page(quiz_page, route="/quiz", title="社交訊號問卷")
app.add_page(login_page, route="/login", title="登入")
app.add_page(
    match_wall_page,
    route="/match",
    title="適合對象",
    on_load=MatchWallState.load_match_wall,
)
app.add_page(
    app_page,
    route="/insight",
    title="分析結果",
    on_load=AppState.load_session_history,
)
app.add_page(
    profile_page,
    route="/profile",
    title="我的訊號",
    on_load=ProfileState.sync_from_disk,
)
app.add_page(
    target_page,
    route="/target",
    title="觀察對象",
    on_load=TargetState.sync_from_disk,
)
