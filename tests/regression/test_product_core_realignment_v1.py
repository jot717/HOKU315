from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_core_realignment_docs_exist() -> None:
    for rel in (
        "docs/archive/product/CORE_PRODUCT_REALIGNMENT.md",
        "docs/archive/product/SOCIAL_SIGNAL_ARCHITECTURE.md",
        "docs/archive/product/HATER_SIGNAL_MODEL.md",
        "docs/deprecated/archive/uat/PRODUCT_DIRECTION_RESET_NOTES.md",
        "backlog/archive/BACKLOG_PRODUCT_CORE_REALIGNMENT_v1.md",
        "backlog/archive/SPRINT_PRODUCT_CORE_REALIGNMENT_v1.md",
    ):
        assert (ROOT / rel).is_file(), rel


def test_core_realignment_defines_product_core() -> None:
    text = _read("docs/archive/product/CORE_PRODUCT_REALIGNMENT.md")
    assert "AI-native SNS guardian" in text or "SNS guardian" in text
    assert "NOT THE PRODUCT" in text or "not the product" in text.lower()
    assert "FOX ROLE" in text


def test_deprecated_language_updated() -> None:
    text = _read("docs/deprecated/DEPRECATED_PRODUCT_LANGUAGE.md")
    assert "AI emotional analysis" in text
    assert "Signal filtering" in text
    assert "social protection" in text


def test_roadmap_phases_defined() -> None:
    text = _read("ops/product/ROADMAP.md")
    assert "Phase 1" in text
    assert "Phase 3" in text and "SNS" in text
    assert "Phase 4" in text
    assert "Phase 5" in text


def test_no_primary_route_breakage_in_fox_quiz_app() -> None:
    """Smoke: main consumer routes still registered (string-level guard)."""
    src = _read("fox_quiz/fox_quiz.py")
    for route in ('route="/"', 'route="/insight"', 'route="/profile"', 'route="/match"'):
        assert route in src, f"missing {route}"
