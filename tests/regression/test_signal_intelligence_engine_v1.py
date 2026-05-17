from __future__ import annotations

from pathlib import Path

from fox_logic import VECTOR_DIM, generate_vector
from fox_quiz.ui.insight_panel import insight_panel
from fox_quiz.ui.profile_page import profile_page
from product.signal.runtime.signal_inference_engine import (
    collect_signal_profile_for_inference,
    infer_signal_risks,
)


ROOT = Path(__file__).resolve().parents[2]


def test_signal_intelligence_docs_exist() -> None:
    for rel in (
        "docs/archive/product/SIGNAL_INTELLIGENCE_CONSTITUTION.md",
        "docs/archive/product/SIGNAL_RISK_ONTOLOGY.md",
        "docs/archive/product/SIGNAL_INFERENCE_MODEL.md",
        "ops/uat/SIGNAL_INTELLIGENCE_ENGINE_UAT.md",
        "backlog/archive/BACKLOG_SIGNAL_INTELLIGENCE_ENGINE_v1.md",
        "backlog/archive/SPRINT_SIGNAL_INTELLIGENCE_ENGINE_v1.md",
    ):
        assert (ROOT / rel).is_file(), rel


def test_ontology_lists_risk_types() -> None:
    text = (ROOT / "ops" / "product" / "SIGNAL_RISK_ONTOLOGY.md").read_text(encoding="utf-8")
    assert "attention_drain_risk" in text
    assert "ghosting_sensitivity" in text


def test_infer_signal_risks_returns_contract() -> None:
    raw = [0.5] * VECTOR_DIM
    raw[3] = 0.9
    raw[9] = 0.92
    vec = generate_vector(raw)
    bundle = {
        "profile": {"name": "t", "interests": [], "activity": 9},
        "memory": {"recent_patterns": [], "recent_warnings": []},
        "mine_vector": vec,
        "insight_state": {"activity_analysis": "some tension"},
        "match_score": 35.0,
    }
    out = infer_signal_risks(bundle)
    assert set(out.keys()) >= {
        "risk_types",
        "risk_scores",
        "guardian_reasoning",
        "high_priority_warning",
        "priority",
        "guardian_action_hint",
    }
    assert out["priority"] in ("HIGH", "MEDIUM", "LOW")
    assert isinstance(out["risk_types"], list)
    assert isinstance(out["risk_scores"], dict)
    assert out["high_priority_warning"]


def test_collect_signal_profile_shape() -> None:
    bundle = collect_signal_profile_for_inference(
        {"activity_analysis": ""},
        50.0,
        None,
    )
    assert "profile" in bundle and "mine_vector" in bundle
    assert len(bundle["mine_vector"]) == VECTOR_DIM


def test_no_onboarding_route_duplicate() -> None:
    src = (ROOT / "fox_quiz" / "fox_quiz.py").read_text(encoding="utf-8")
    assert 'route="/onboarding' not in src


def test_insight_and_profile_still_compile() -> None:
    assert insight_panel() is not None
    assert profile_page() is not None
