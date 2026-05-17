from __future__ import annotations

from fox_quiz.ui.app_page import app_page
from fox_quiz.ui.components.world_container import world_container
from fox_quiz.ui.insight_panel import insight_panel


def test_active_shell_compiles() -> None:
    assert app_page() is not None
    assert world_container(insight_panel()) is not None
    assert insight_panel() is not None
