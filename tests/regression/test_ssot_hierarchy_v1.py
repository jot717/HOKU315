from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SSOT_SECTIONS = (
    "Product SSOT",
    "Governance SSOT",
    "Planning SSOT",
    "Sprint SSOT",
    "Execution SSOT",
    "Archive rules",
    "Authority precedence rules",
)


def test_ssot_hierarchy_exists_with_sections() -> None:
    path = ROOT / "docs/active/governance/SSOT_HIERARCHY.md"
    text = path.read_text(encoding="utf-8")
    assert path.is_file()
    for section in SSOT_SECTIONS:
        assert section in text, f"missing section: {section}"


def test_roadmap_phases_one_through_seven() -> None:
    text = (ROOT / "docs/active/product/ROADMAP.md").read_text(encoding="utf-8")
    for n in range(1, 8):
        assert f"PHASE{n}" in text
    assert "inferring phases" in text.lower() or "never plan from archive" in text.lower()
    assert "FOX_ROADMAP" in text


def test_start_new_sprint_authority_chain() -> None:
    text = (ROOT / "docs/active/governance/START_NEW_SPRINT.md").read_text(encoding="utf-8")
    assert "SSOT_HIERARCHY" in text
    assert "ROADMAP.md" in text
    assert "MASTER_BACKLOG" in text
    assert "IMPLEMENT" in text and "ARCHIVE" in text


def test_no_active_fox_roadmap() -> None:
    assert not (ROOT / "docs/active/product/FOX_ROADMAP.md").exists()


def test_master_backlog_points_to_roadmap_not_duplicate_phases() -> None:
    text = (ROOT / "docs/active/governance/MASTER_BACKLOG.md").read_text(encoding="utf-8")
    assert "ROADMAP.md" in text
    assert "PHASE7" in text or "Platform" in text
