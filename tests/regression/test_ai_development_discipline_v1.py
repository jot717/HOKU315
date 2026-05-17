from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ROOT_MD_ALLOWED = {"README.md", "BACKLOG.md", "SPRINT_LOG.md"}
ARCHIVE_LINK = re.compile(r"\]\([^)]*docs/archive/[^)]+\)", re.I)
GOVERNANCE_EXCLUDE_ARCHIVE_LINKS = {
    "START_NEW_SPRINT.md",
    "REPO_GOVERNANCE_RULES.md",
    "REPO_ENTROPY_CHECKLIST.md",
    "MASTER_BACKLOG.md",
    "AI_CONTEXT_PRIORITY.md",
}


def test_start_new_sprint_exists() -> None:
    path = ROOT / "docs/active/governance/START_NEW_SPRINT.md"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "START NEW SPRINT" in text
    assert "PRODUCT_MASTER" in text
    assert "SSOT_HIERARCHY" in text
    assert "ROADMAP.md" in text
    assert "IMPLEMENT" in text and "ARCHIVE" in text
    assert "FORBIDDEN AI BEHAVIORS" in text
    assert "parallel constitutions" in text.lower() or "parallel" in text.lower()


def test_ai_task_template_exists() -> None:
    path = ROOT / "docs/active/governance/AI_TASK_TEMPLATE.md"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "START_NEW_SPRINT" in text
    assert "SSOT only" in text


def test_root_markdown_not_expanded() -> None:
    assert {p.name for p in ROOT.glob("*.md")} == ROOT_MD_ALLOWED


def test_governance_no_archive_authority_links() -> None:
    for path in (ROOT / "docs/active/governance").glob("*.md"):
        if path.name in GOVERNANCE_EXCLUDE_ARCHIVE_LINKS:
            continue
        hits = ARCHIVE_LINK.findall(path.read_text(encoding="utf-8"))
        assert not hits, f"{path.name} links docs/archive as authority: {hits[:3]}"


def test_readme_points_to_start_new_sprint() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "AI DEVELOPMENT ENTRY" in text
    assert "START_NEW_SPRINT.md" in text


def test_product_master_points_to_start_new_sprint() -> None:
    text = (ROOT / "docs/active/product/PRODUCT_MASTER.md").read_text(encoding="utf-8")
    assert "AI DEVELOPMENT DISCIPLINE" in text
    assert "START_NEW_SPRINT.md" in text


def test_governance_checklist_discipline_items() -> None:
    text = (ROOT / "docs/active/governance/GOVERNANCE_CHECKLIST.md").read_text(encoding="utf-8")
    for item in (
        "START_NEW_SPRINT loaded",
        "PRODUCT_MASTER loaded",
        "MASTER_BACKLOG loaded",
        "no archive context used",
        "no duplicate docs created",
        "phase boundary respected",
    ):
        assert item in text, f"missing checklist item: {item}"
