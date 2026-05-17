from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ARCHIVED_STORY = ROOT / "docs/archive/dead_routes/story_page.py"

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


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_quiz_and_login_sources_have_no_premature_api_copy() -> None:
    quiz_src = _read("fox_quiz/fox_quiz.py")
    _assert_clean("fox_quiz.py", quiz_src)
    _assert_clean("login_page.py", _read("fox_quiz/login_page.py"))


def test_archived_story_reference_has_no_premature_api_copy() -> None:
    assert ARCHIVED_STORY.is_file()
    _assert_clean("archived story_page", ARCHIVED_STORY.read_text(encoding="utf-8"))


def test_match_insight_profile_sources_clean() -> None:
    _assert_clean("match_wall.py", _read("fox_quiz/match_wall.py"))
    _assert_clean("insight_panel.py", _read("fox_quiz/ui/insight_panel.py"))
    _assert_clean("profile_page.py", _read("fox_quiz/ui/profile_page.py"))
