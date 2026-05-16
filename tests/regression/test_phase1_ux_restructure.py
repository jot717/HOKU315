from __future__ import annotations

from pathlib import Path

from fox_quiz.state.profile_state import PROFILE_SAVE_SUCCESS_MESSAGE
from fox_quiz.ui.insight_panel import insight_panel


ROOT = Path(__file__).resolve().parents[2]


def test_signal_first_product_position_exists() -> None:
    path = ROOT / "ops" / "product" / "SIGNAL_FIRST_PRODUCT_POSITION.md"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "Signal-first UX law" in text
    assert "AI-native social signal intelligence" in text


def test_phase1_product_flow_uat_exists() -> None:
    path = ROOT / "ops" / "uat" / "PHASE1_PRODUCT_FLOW_UAT.md"
    assert path.is_file()


def test_phase1_product_flow_recovery_backlog_sprint_exist() -> None:
    assert (ROOT / "backlog" / "BACKLOG_PHASE1_PRODUCT_FLOW_RECOVERY_v1.md").is_file()
    assert (ROOT / "backlog" / "SPRINT_PHASE1_PRODUCT_FLOW_RECOVERY_v1.md").is_file()


def test_deprecated_guardian_constitution_archived() -> None:
    path = ROOT / "docs" / "deprecated" / "GUARDIAN_UX_CONSTITUTION.md"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "SIGNAL-FIRST" in text


def test_profile_save_success_message_signal_profile() -> None:
    assert "社交訊號檔案" in PROFILE_SAVE_SUCCESS_MESSAGE


def test_insight_next_actions_labels() -> None:
    panel_src = (ROOT / "fox_quiz" / "ui" / "insight_panel.py").read_text(encoding="utf-8")
    assert "重新分析" in panel_src
    assert "更新我的訊號" in panel_src
    assert "查看適合對象" in panel_src


def test_home_page_signal_first_hook_copy() -> None:
    home_src = (ROOT / "fox_quiz" / "ui" / "pages" / "home_page.py").read_text(encoding="utf-8")
    assert "AI 社交訊號分析系統" in home_src
    assert "建立你的社交訊號檔案" in home_src


def test_profile_page_signal_profile_copy() -> None:
    prof_src = (ROOT / "fox_quiz" / "ui" / "profile_page.py").read_text(encoding="utf-8")
    assert "危險互動分析" in prof_src
    assert "開始訊號問卷" in prof_src


def test_insight_panel_compiles() -> None:
    assert insight_panel() is not None
