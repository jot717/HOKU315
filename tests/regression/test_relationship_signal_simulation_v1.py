from __future__ import annotations

from pathlib import Path

from fox_quiz.ui.insight_panel import insight_panel
from fox_quiz.ui.pages.home_page import home_page
from product.signal.runtime.relationship_simulation_engine import (
    generate_relationship_archetype,
    simulate_relationship_risk,
)

ROOT = Path(__file__).resolve().parents[2]


def test_relationship_intelligence_docs_exist() -> None:
    for rel in (
        "docs/archive/product/RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md",
        "docs/archive/product/RELATIONSHIP_ARCHETYPE_MODEL.md",
        "docs/archive/product/INTERACTION_SIGNAL_ONTOLOGY.md",
        "docs/archive/uat/RELATIONSHIP_SIGNAL_SIMULATION_UAT.md",
        "backlog/archive/BACKLOG_RELATIONSHIP_SIGNAL_SIMULATION_v1.md",
        "backlog/archive/SPRINT_RELATIONSHIP_SIGNAL_SIMULATION_v1.md",
    ):
        assert (ROOT / rel).is_file(), rel


def test_generate_relationship_archetype_contract() -> None:
    arch = generate_relationship_archetype()
    assert set(arch.keys()) == {
        "archetype_name",
        "interaction_signals",
        "danger_summary",
        "guardian_warning",
        "risk_pressure",
    }
    assert arch["archetype_name"]
    assert isinstance(arch["interaction_signals"], list)
    assert arch["risk_pressure"] in ("LOW", "MEDIUM", "HIGH")


def test_simulate_relationship_risk_contract() -> None:
    arch = generate_relationship_archetype()
    out = simulate_relationship_risk(
        {
            "risk_scores": {"emotional_exhaustion_risk": 0.9},
            "profile": {"activity": 8},
        },
        arch,
    )
    assert set(out.keys()) == {
        "interaction_risk_score",
        "risk_matches",
        "danger_explanation",
        "guardian_advice",
    }
    assert 0 <= out["interaction_risk_score"] <= 100
    assert isinstance(out["risk_matches"], list)
    assert isinstance(out["danger_explanation"], list)
    assert out["guardian_advice"]


def test_fox_quiz_routes_still_defined() -> None:
    src = (ROOT / "fox_quiz" / "fox_quiz.py").read_text(encoding="utf-8")
    assert 'route="/insight"' in src
    assert 'route="/home"' in src or 'route="/"' in src


def test_insight_and_home_still_compile() -> None:
    assert insight_panel() is not None
    assert home_page() is not None
