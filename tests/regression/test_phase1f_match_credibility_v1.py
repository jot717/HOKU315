from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from fox_quiz.match_wall import enrich_match_row_for_ui, match_wall_page
from fox_quiz.ui.insight_panel import insight_panel
from product.match.runtime import match_rhythm_engine as mre

ROOT = Path(__file__).resolve().parents[2]

_FORBIDDEN = (
    "trauma",
    "attachment style",
    "MBTI",
    "心理治療",
    "人格障礙",
    "你太敏感",
    "dating score",
    "星座",
    "相容度：高",
)


def test_match_archetype_docs_exist() -> None:
    arch = (ROOT / "ops/product/MATCH_ARCHETYPE_SYSTEM.md").read_text(encoding="utf-8")
    assert "stable_low_pressure" in arch
    assert "asynchronous_safe" in arch
    energy = (ROOT / "ops/product/SOCIAL_ENERGY_MODEL.md").read_text(encoding="utf-8")
    assert "response debt" in energy
    assert (ROOT / "ops/product/MATCH_CREDIBILITY_CONSTITUTION.md").is_file()
    assert (ROOT / "ops/uat/PHASE1F_MATCH_CREDIBILITY_UAT.md").is_file()


def test_rhythm_engine_functions_exist() -> None:
    for name in (
        "infer_social_rhythm",
        "infer_energy_cost",
        "infer_response_pressure",
        "infer_interaction_stability",
        "generate_match_credibility_bundle",
        "generate_insight_weakness_link",
    ):
        assert hasattr(mre, name)
        assert callable(getattr(mre, name))


def test_credibility_bundle_card_fields() -> None:
    cred = mre.generate_match_credibility_bundle(
        distance=0.28,
        compat_bucket="h",
        conflict_dim_label="dm_pace_sensitivity",
        blurred=False,
        user_inference={"risk_scores": {"ghosting_sensitivity": 0.7}},
    )
    for key in (
        "interaction_rhythm_line",
        "reply_pressure_line",
        "emotional_pacing_line",
        "energy_safety_line",
        "exhaustion_point_line",
        "scenario_line",
    ):
        assert cred[key]
    blob = " ".join(cred.values()).lower()
    for bad in _FORBIDDEN:
        assert bad.lower() not in blob, bad


def test_insight_weakness_link_is_causal() -> None:
    line = mre.generate_insight_weakness_link(
        inference={"risk_scores": {"ghosting_sensitivity": 0.75}},
    )
    assert "待太久" in line
    assert "節奏" in line


def test_enrich_row_has_credibility_keys() -> None:
    row = enrich_match_row_for_ui(
        {"distance": 0.3, "is_blurred": False, "conflict_dim_label": "x"},
        0,
    )
    assert row["interaction_rhythm_line"]
    assert row["reply_pressure_line"]
    assert row["energy_badge"] in ("偏高", "偏低", "中等")


def test_match_wall_no_dating_vibe_copy() -> None:
    src = inspect.getsource(match_wall_page)
    assert "相容度：高" not in src
    assert "社交電量" in src


def test_insight_single_fox_block() -> None:
    src = (ROOT / "fox_quiz/ui/insight_panel.py").read_text(encoding="utf-8")
    assert src.count("北極狐觀察") == 1
    assert "北極狐提醒" not in src


def test_pages_compile() -> None:
    assert match_wall_page() is not None
    assert insight_panel() is not None
