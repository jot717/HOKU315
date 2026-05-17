from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from fox_quiz.match_wall import enrich_match_row_for_ui, match_wall_page
from fox_quiz.ui.insight_panel import insight_panel
from product.signal.runtime import ux_intelligence_engine as uxe

ROOT = Path(__file__).resolve().parents[2]

_THERAPY_FORBIDDEN = (
    "trauma",
    "attachment style",
    "inner child",
    "healing journey",
    "心理治療",
    "人格障礙",
    "憂鬱症",
    "焦慮症",
    "你不夠自信",
    "emotionally insecure",
)

_DIAG_FORBIDDEN = (
    "診斷",
    "臨床",
    "NPD",
    "ADHD",
)


def test_ontology_doc_exists() -> None:
    path = ROOT / "docs/archive/phase1_legacy/INTERACTION_PRESSURE_ONTOLOGY.md"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    for pattern in (
        "emotional_labor_trap",
        "response_pressure",
        "conflict_avoidance_exhaustion",
    ):
        assert pattern in text


def test_ux_engine_functions_exist() -> None:
    for name in (
        "generate_interaction_reasoning",
        "generate_pressure_explanations",
        "generate_match_fit_reasoning",
        "generate_avoidance_reasoning",
    ):
        assert hasattr(uxe, name)
        assert callable(getattr(uxe, name))


def test_generate_interaction_reasoning_contract() -> None:
    out = uxe.generate_interaction_reasoning(
        profile={"activity": 7},
        inference={
            "risk_scores": {"ghosting_sensitivity": 0.8},
            "risk_types": ["ghosting_sensitivity"],
            "priority": "MEDIUM",
        },
        archetype={
            "archetype_name": "示範",
            "interaction_signals": ["delayed reassurance"],
            "danger_summary": "節奏搖擺。",
        },
        match_score=55.0,
    )
    assert out["why_drains"]
    assert out["rhythm_conflict"]
    assert isinstance(out["pressure_bullets"], list)
    assert out["fit_reasoning"]
    assert out["avoid_reasoning"]
    assert out["fox_observer"]
    combined = " ".join(
        [
            out["why_drains"],
            out["fox_observer"],
            out["avoid_reasoning"],
        ]
    ).lower()
    for bad in _THERAPY_FORBIDDEN + _DIAG_FORBIDDEN:
        assert bad.lower() not in combined, bad


def test_match_fit_reasoning_has_scenario() -> None:
    ux = uxe.generate_match_fit_reasoning(
        distance=0.25,
        compat_bucket="h",
        conflict_dim_label="dm_pace",
        blurred=False,
        inference={"risk_scores": {"attention_drain_risk": 0.6}},
    )
    assert ux["lighter_line"]
    assert ux["scenario_line"]
    assert "例如" in ux["scenario_line"]


def test_enrich_match_row_includes_ux_lines() -> None:
    row = enrich_match_row_for_ui(
        {"distance": 0.3, "is_blurred": False, "conflict_dim_label": "x"},
        0,
    )
    for key in (
        "emotion_line",
        "rhythm_line",
        "match_rationale_line",
        "fatigue_avoided_line",
        "scenario_line",
    ):
        assert key in row
        assert row[key]


def test_insight_panel_single_fox_block() -> None:
    src = (ROOT / "fox_quiz/ui/insight_panel.py").read_text(encoding="utf-8")
    assert src.count("北極狐觀察") == 1
    assert "北極狐提醒" not in src
    assert src.count("_section_fox_observer") >= 2  # def + call in column


def test_insight_and_match_pages_build() -> None:
    assert insight_panel() is not None
    assert match_wall_page() is not None


def test_phase1d_docs_exist() -> None:
    for rel in (
        "docs/archive/phase1_legacy/UX_INTELLIGENCE_CONSTITUTION.md",
        "docs/archive/phase1_legacy/SOCIAL_CAUSALITY_RULES.md",
        "ops/product/SIGNAL_SYSTEM.md",
        "docs/archive/old_uat/PHASE1D_UX_INTELLIGENCE_UAT.md",
    ):
        assert (ROOT / rel).is_file(), rel
