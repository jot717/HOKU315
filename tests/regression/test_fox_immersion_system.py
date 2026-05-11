from __future__ import annotations

from fox_quiz.ui.app_page import app_page
from fox_quiz.ui.components.fox_avatar import fox_avatar
from fox_quiz.ui.insight_panel import insight_panel


def test_fox_immersion_system_compiles() -> None:
    assert app_page() is not None
    assert fox_avatar() is not None
    assert insight_panel() is not None
