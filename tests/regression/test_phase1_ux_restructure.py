from __future__ import annotations

from pathlib import Path

from fox_quiz.state.profile_state import PROFILE_SAVE_SUCCESS_MESSAGE
from fox_quiz.ui.insight_panel import insight_panel


ROOT = Path(__file__).resolve().parents[2]


def test_guardian_ux_constitution_exists() -> None:
    path = ROOT / "ops" / "product" / "GUARDIAN_UX_CONSTITUTION.md"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "PRODUCT IDENTITY" in text
    assert "FORBIDDEN UX PATTERNS" in text
    assert "UX HIERARCHY" in text


def test_phase1_ux_restructure_uat_notes_exist() -> None:
    path = ROOT / "ops" / "uat" / "PHASE1_UX_RESTRUCTURE_NOTES.md"
    assert path.is_file()


def test_phase1_ux_restructure_backlog_sprint_docs_exist() -> None:
    assert (ROOT / "backlog" / "BACKLOG_PHASE1_UX_RESTRUCTURE_v1.md").is_file()
    assert (ROOT / "backlog" / "SPRINT_PHASE1_UX_RESTRUCTURE_v1.md").is_file()


def test_profile_save_success_message_observatory_cta() -> None:
    assert "觀察室" in PROFILE_SAVE_SUCCESS_MESSAGE


def test_insight_next_actions_labels() -> None:
    panel_src = (ROOT / "fox_quiz" / "ui" / "insight_panel.py").read_text(encoding="utf-8")
    assert "重新觀察" in panel_src
    assert "更新我的訊號" in panel_src
    assert "查看守護筆記" in panel_src


def test_home_page_guardian_hook_copy() -> None:
    home_src = (ROOT / "fox_quiz" / "ui" / "pages" / "home_page.py").read_text(encoding="utf-8")
    assert "有些危險" in home_src
    assert "交友軟體" in home_src
    assert "守護視角" in home_src or "過濾" in home_src


def test_profile_page_fox_data_purpose_copy() -> None:
    prof_src = (ROOT / "fox_quiz" / "ui" / "profile_page.py").read_text(encoding="utf-8")
    assert "北極狐會透過這些訊號" in prof_src
    assert "進入觀察室" in prof_src


def test_insight_panel_compiles() -> None:
    assert insight_panel() is not None
