from __future__ import annotations

from pathlib import Path

import pytest

from fox_quiz.ui.insight_panel import insight_panel
from fox_quiz.ui.pages.target_page import target_page
from product.signal.runtime.relationship_simulation_engine import (
    archetype_for_target_profile,
    build_virtual_partner_profile,
    generate_relationship_archetype,
    simulate_relationship_risk,
)
from product.target.runtime import target_profile_store as tps

ROOT = Path(__file__).resolve().parents[2]


def test_target_signal_docs_exist() -> None:
    for rel in (
        "docs/archive/product/TARGET_SIGNAL_CONSTITUTION.md",
        "docs/archive/product/TARGET_ANALYSIS_FLOW.md",
        "docs/archive/product/TARGET_PROFILE_SCHEMA.md",
        "ops/uat/TARGET_SIGNAL_PROFILE_UAT.md",
        "backlog/archive/BACKLOG_TARGET_SIGNAL_PROFILE_v1.md",
        "backlog/archive/SPRINT_TARGET_SIGNAL_PROFILE_v1.md",
    ):
        assert (ROOT / rel).is_file(), rel


def test_target_route_registered() -> None:
    src = (ROOT / "fox_quiz" / "fox_quiz.py").read_text(encoding="utf-8")
    assert 'route="/target"' in src


def test_target_store_roundtrip(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    p = tmp_path / "target_profile.json"
    monkeypatch.setattr(tps, "TARGET_PATH", p)
    payload = {
        "target_name": "測試對象",
        "relationship_type": "同事",
        "observed_traits": ["常改期"],
        "communication_style": ["短句"],
        "social_patterns": [],
        "pressure_signals": ["比較"],
        "instability_level": 7,
        "attention_demand": 6,
        "response_consistency": 3,
        "notes": "demo",
    }
    tps.save_target_profile(payload)
    loaded = tps.load_target_profile()
    assert loaded["target_name"] == "測試對象"
    assert loaded["instability_level"] == 7
    assert "常改期" in loaded["observed_traits"]


def test_archetype_for_target_profile_returns_contract() -> None:
    arch = archetype_for_target_profile(
        {
            "target_name": "X",
            "observed_traits": ["已讀不回", "消失"],
            "instability_level": 2,
            "attention_demand": 2,
            "response_consistency": 1,
        }
    )
    assert set(arch.keys()) == {
        "archetype_name",
        "interaction_signals",
        "danger_summary",
        "guardian_warning",
        "risk_pressure",
    }
    assert arch["archetype_name"]


def test_build_virtual_partner_profile() -> None:
    b = build_virtual_partner_profile(
        {
            "observed_traits": ["閱讀", "跑步"],
            "instability_level": 8,
            "attention_demand": 8,
        }
    )
    assert "activity" in b and "interests" in b
    assert isinstance(b["interests"], list)


def test_simulate_relationship_risk_accepts_optional_target() -> None:
    arch = generate_relationship_archetype()
    base = simulate_relationship_risk(
        {"risk_scores": {"emotional_exhaustion_risk": 0.5}, "profile": {"activity": 5}},
        arch,
    )
    with_target = simulate_relationship_risk(
        {"risk_scores": {"emotional_exhaustion_risk": 0.5}, "profile": {"activity": 5}},
        arch,
        {"attention_demand": 10, "instability_level": 10, "response_consistency": 0},
    )
    assert "interaction_risk_score" in base and "interaction_risk_score" in with_target
    assert with_target["interaction_risk_score"] >= base["interaction_risk_score"]


def test_insight_and_target_pages_compile() -> None:
    assert insight_panel() is not None
    assert target_page() is not None
