from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_core_realignment_docs_exist() -> None:
    for rel in (
        "ops/product/CORE_PRODUCT_REALIGNMENT.md",
        "ops/product/SOCIAL_SIGNAL_ARCHITECTURE.md",
        "ops/product/HATER_SIGNAL_MODEL.md",
        "ops/uat/PRODUCT_DIRECTION_RESET_NOTES.md",
        "backlog/BACKLOG_PRODUCT_CORE_REALIGNMENT_v1.md",
        "backlog/SPRINT_PRODUCT_CORE_REALIGNMENT_v1.md",
    ):
        assert (ROOT / rel).is_file(), rel


def test_core_realignment_defines_product_core() -> None:
    text = _read("ops/product/CORE_PRODUCT_REALIGNMENT.md")
    assert "AI-native SNS guardian" in text or "SNS guardian" in text
    assert "NOT THE PRODUCT" in text or "not the product" in text.lower()
    assert "FOX ROLE" in text


def test_deprecated_language_updated() -> None:
    text = _read("docs/deprecated/DEPRECATED_PRODUCT_LANGUAGE.md")
    assert "AI emotional analysis" in text
    assert "Signal filtering" in text
    assert "social protection" in text


def test_fox_roadmap_realigned_phases() -> None:
    text = _read("ops/product/FOX_ROADMAP.md")
    assert "PHASE 1" in text and "Guardian UX MVP" in text
    assert "PHASE 3" in text and "SNS Ingestion" in text
    assert "PHASE 4" in text and "Social Graph" in text
    assert "PHASE 6" in text and "AI Signal Scale" in text


def test_no_primary_route_breakage_in_fox_quiz_app() -> None:
    """Smoke: main consumer routes still registered (string-level guard)."""
    src = _read("fox_quiz/fox_quiz.py")
    for route in ('route="/"', 'route="/insight"', 'route="/profile"', 'route="/match"'):
        assert route in src, f"missing {route}"
