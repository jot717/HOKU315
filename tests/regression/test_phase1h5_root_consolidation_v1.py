from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ROOT_MD_ALLOWED = {"README.md", "BACKLOG.md", "SPRINT_LOG.md"}
PRODUCT_SSOT = {
    "PRODUCT_MASTER.md",
    "AI_DEVELOPMENT_CONSTITUTION.md",
    "MATCH_SYSTEM.md",
    "SIGNAL_SYSTEM.md",
    "ROADMAP.md",
    "CANONICAL_TERMINOLOGY.md",
    "ACTIVE_SURFACE_MAP.md",
}
GOVERNANCE_FILES = {
    "MASTER_BACKLOG.md",
    "REPO_GOVERNANCE_RULES.md",
    "GOVERNANCE_CHECKLIST.md",
    "AI_CONTEXT_PRIORITY.md",
    "REPO_ENTROPY_CHECKLIST.md",
    "DEVELOPMENT_CONSTITUTION.md",
    "ARCHITECTURE_CONTRACT.md",
    "REPO_ARCHITECTURE.md",
}
OPS_ALLOWED = {"env", "flow", "debug", "testing"}


def test_root_markdown_lobby_only() -> None:
    assert {p.name for p in ROOT.glob("*.md")} == ROOT_MD_ALLOWED


def test_product_ssot_seven_files() -> None:
    found = {p.name for p in (ROOT / "docs/active/product").glob("*.md") if p.name != "README.md"}
    assert found == PRODUCT_SSOT


def test_governance_layer_complete() -> None:
    found = {p.name for p in (ROOT / "docs/active/governance").glob("*.md") if p.name != "README.md"}
    assert GOVERNANCE_FILES <= found


def test_master_backlog_not_in_backlog_folder() -> None:
    assert (ROOT / "docs/active/governance/MASTER_BACKLOG.md").is_file()
    assert not (ROOT / "backlog/MASTER_BACKLOG.md").exists()


def test_ops_only_executable_dirs() -> None:
    dirs = {p.name for p in (ROOT / "ops").iterdir() if p.is_dir()}
    extra = dirs - OPS_ALLOWED - {"product", "uat", "env"}
    assert not extra, f"unexpected ops dirs: {extra}"
    assert (ROOT / "ops/product/README.md").is_file()


def test_ai_constitution_load_order() -> None:
    text = (ROOT / "docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md").read_text(encoding="utf-8")
    assert "AI CONTEXT LOAD ORDER" in text
    assert "AI MUST IGNORE" in text


def test_root_readme_is_lobby() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "START HERE" in text
    assert "docs/README.md" in text
    assert len(text) < 2500
