from __future__ import annotations

import inspect

import pytest

from fox_quiz.fox_quiz import QuizState, quiz_page
from fox_quiz.login_page import LoginState, login_page
from fox_quiz.match_wall import match_wall_page
from fox_quiz.story_page import StoryState, story_page
from fox_quiz.ui.insight_panel import insight_panel
from fox_quiz.ui.profile_page import profile_page

try:
    from fox_quiz.chat_component import chat_page
except Exception:  # pragma: no cover
    chat_page = None


# User-visible / premature SNS–API leakage (Phase1 must not show these in page sources).
_FORBIDDEN_SUBSTRINGS = (
    "同步失敗",
    "MOCK_LOGIN",
    "DB_TEST_PROFILE_ID",
    "貼上 access",
    "Supabase Auth",
    "JWT",
    "user_id/",
    "無法同步 profiles",
    "雲端脈絡",
    "token 存於裝置",
    "OAuth",
    "oauth",
    "Graph API",
    "social graph",
)


def _assert_clean(label: str, src: str) -> None:
    for bad in _FORBIDDEN_SUBSTRINGS:
        if bad in src:
            pytest.fail(f"{label}: forbidden Phase1 substring {bad!r} found in source")
        if bad.isascii() and bad.lower() in src.lower():
            pytest.fail(f"{label}: forbidden Phase1 substring {bad!r} found in source")


def _handler_source(cls: type, method_name: str) -> str:
    m = getattr(cls, method_name)
    fn = getattr(m, "fn", m)
    return inspect.getsource(fn)


def test_quiz_state_and_page_have_no_premature_api_copy() -> None:
    _assert_clean("QuizState.generate_result", _handler_source(QuizState, "generate_result"))
    _assert_clean("quiz_page", inspect.getsource(quiz_page))


def test_login_flow_has_no_premature_api_copy() -> None:
    _assert_clean("login_page", inspect.getsource(login_page))
    _assert_clean("LoginState.submit_login", _handler_source(LoginState, "submit_login"))
    _assert_clean("LoginState.submit_signup", _handler_source(LoginState, "submit_signup"))


def test_story_flow_has_no_premature_api_copy() -> None:
    _assert_clean("story_page", inspect.getsource(story_page))
    _assert_clean("StoryState.submit_story", _handler_source(StoryState, "submit_story"))


def test_match_insight_profile_pages_compile_clean_copy() -> None:
    _assert_clean("match_wall_page", inspect.getsource(match_wall_page))
    _assert_clean("insight_panel", inspect.getsource(insight_panel))
    _assert_clean("profile_page", inspect.getsource(profile_page))


@pytest.mark.skipif(chat_page is None, reason="chat_page import failed")
def test_chat_page_optional_clean_copy() -> None:
    _assert_clean("chat_page", inspect.getsource(chat_page))


def test_phase1_pages_build() -> None:
    assert quiz_page() is not None
    assert login_page() is not None
    assert story_page() is not None
    assert match_wall_page() is not None
    assert insight_panel() is not None
    assert profile_page() is not None
