from __future__ import annotations

from pathlib import Path

from fox_quiz.ui.insight_panel import insight_panel
from fox_quiz.ui.pages.home_page import home_page
from fox_quiz.ui.profile_page import profile_page


ROOT = Path(__file__).resolve().parents[2]


def test_signal_consolidation_product_docs_exist() -> None:
    for rel in (
        "ops/product/SIGNAL_SYSTEM_CONSTITUTION.md",
        "ops/product/SIGNAL_PROFILE_SCHEMA.md",
        "ops/product/SIGNAL_FLOW_ARCHITECTURE.md",
        "ops/product/SIGNAL_INPUT_AUDIT.md",
        "ops/product/SIGNAL_STATE_MAPPING.md",
    ):
        assert (ROOT / rel).is_file(), rel


def test_signal_consolidation_uat_and_backlog_exist() -> None:
    assert (ROOT / "ops" / "uat" / "SIGNAL_SYSTEM_CONSOLIDATION_UAT.md").is_file()
    assert (ROOT / "backlog" / "BACKLOG_SIGNAL_SYSTEM_CONSOLIDATION_v1.md").is_file()
    assert (ROOT / "backlog" / "SPRINT_SIGNAL_SYSTEM_CONSOLIDATION_v1.md").is_file()


def test_canonical_schema_doc_contains_identity_signals() -> None:
    schema = (ROOT / "ops" / "product" / "SIGNAL_PROFILE_SCHEMA.md").read_text(encoding="utf-8")
    assert '"identity_signals"' in schema
    assert "signal_history" in schema


def test_guardian_constitution_has_signal_first_rule() -> None:
    text = (ROOT / "ops" / "product" / "GUARDIAN_UX_CONSTITUTION.md").read_text(encoding="utf-8")
    assert "SIGNAL-FIRST" in text
    assert "signal intelligence" in text


def test_fox_roadmap_mentions_signal_consolidation() -> None:
    text = (ROOT / "ops" / "product" / "FOX_ROADMAP.md").read_text(encoding="utf-8")
    assert "SIGNAL_SYSTEM_CONSTITUTION" in text


def test_no_duplicate_onboarding_route_added() -> None:
    src = (ROOT / "fox_quiz" / "fox_quiz.py").read_text(encoding="utf-8")
    assert 'route="/onboarding' not in src


def test_primary_routes_unchanged_in_fox_quiz_app() -> None:
    src = (ROOT / "fox_quiz" / "fox_quiz.py").read_text(encoding="utf-8")
    for route in ('route="/"', 'route="/insight"', 'route="/profile"', 'route="/quiz"'):
        assert route in src, route


def test_profile_and_insight_pages_still_compile() -> None:
    assert profile_page() is not None
    assert insight_panel() is not None
    assert home_page() is not None
