from fox_quiz.ui.app_page import app_page
from fox_quiz.ui.components.hero_insight import hero_insight
from fox_quiz.ui.insight_panel import insight_panel


def test_app_experience_polish_imports_and_compile():
    assert app_page() is not None
    assert hero_insight() is not None
    assert insight_panel() is not None
