from __future__ import annotations

from fox_quiz.ui.insight_panel import (
    insight_next_actions_section,
    insight_onboarding_explanation_card,
    insight_panel,
    insight_result_explanation_section,
    insight_why_bullets_section,
)
from fox_quiz.ui.profile_page import profile_page


def test_phase1_uat_flow_pages_compile() -> None:
    assert profile_page() is not None
    assert insight_panel() is not None


def test_phase1_uat_onboarding_and_next_actions_render() -> None:
    assert insight_onboarding_explanation_card() is not None
    assert insight_why_bullets_section() is not None
    assert insight_result_explanation_section() is not None
    assert insight_next_actions_section() is not None
