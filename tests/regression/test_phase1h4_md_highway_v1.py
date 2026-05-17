from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ROOT_MD_ALLOWED = {"README.md", "BACKLOG.md", "SPRINT_LOG.md"}
ACTIVE_PRODUCT_FILES = {
    "PRODUCT_MASTER.md",
    "SIGNAL_SYSTEM.md",
    "MATCH_SYSTEM.md",
    "ROADMAP.md",
    "AI_DEVELOPMENT_CONSTITUTION.md",
    "CANONICAL_TERMINOLOGY.md",
    "ACTIVE_SURFACE_MAP.md",
    "REPO_GOVERNANCE_RULES.md",
}
ACTIVE_UAT_FILES = {"UAT_MASTER_GUIDE.md", "PHASE1_PRODUCT_FLOW_UAT.md"}


def test_root_markdown_minimal() -> None:
    root_md = {p.name for p in ROOT.glob("*.md")}
    assert root_md == ROOT_MD_ALLOWED, root_md


def test_active_product_ssot_files() -> None:
    found = {p.name for p in (ROOT / "docs/active/product").glob("*.md") if p.name != "README.md"}
    assert found == ACTIVE_PRODUCT_FILES, found


def test_active_uat_files() -> None:
    found = {p.name for p in (ROOT / "docs/active/uat").glob("*.md") if p.name != "README.md"}
    assert found == ACTIVE_UAT_FILES, found


def test_governance_files_moved_from_root() -> None:
    assert (ROOT / "ops/governance/DEVELOPMENT_CONSTITUTION.md").is_file()
    assert (ROOT / "ops/debug/DEBUG_GUIDE.md").is_file()
    assert (ROOT / "ops/testing/TEST_CHECKLIST.md").is_file()
    assert not (ROOT / "DEVELOPMENT_CONSTITUTION.md").exists()


def test_md_highway_readmes() -> None:
    for rel in (
        "docs/README.md",
        "docs/active/README.md",
        "docs/archive/README.md",
        "ops/README.md",
        "backlog/README.md",
    ):
        assert (ROOT / rel).is_file(), rel


def test_ai_constitution_highway_rules() -> None:
    text = (ROOT / "docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md").read_text(encoding="utf-8")
    assert "Section I" in text
    assert "docs/active/" in text
    assert "Never create" in text and "root" in text.lower()


def test_archive_buckets_exist() -> None:
    archive = ROOT / "docs/archive"
    for name in ("product", "uat", "hotfix", "legacy", "dead_routes", "root_legacy"):
        assert (archive / name).is_dir(), name
    loose = [p.name for p in archive.glob("*.md") if p.name != "README.md"]
    assert not loose, loose


def test_ops_product_is_pointer_only() -> None:
    md = list((ROOT / "ops/product").glob("*.md"))
    assert len(md) == 1 and md[0].name == "README.md"
