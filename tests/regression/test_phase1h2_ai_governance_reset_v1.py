from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ACTIVE_PRODUCT_MAX = 10
ACTIVE_UAT_MAX = 5

GOVERNANCE_FILES = (
    "docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md",
    "docs/active/product/CANONICAL_TERMINOLOGY.md",
    "docs/active/governance/GOVERNANCE_CHECKLIST.md",
    "docs/active/product/ACTIVE_SURFACE_MAP.md",
)

SSOT_FILES = (
    "docs/active/product/PRODUCT_MASTER.md",
    "docs/active/product/SIGNAL_SYSTEM.md",
    "docs/active/product/MATCH_SYSTEM.md",
    "docs/active/product/ROADMAP.md",
)

UAT_AUDIT_EXCLUDE: set[str] = set()


def _active_product_docs() -> list[Path]:
    return [p for p in (ROOT / "docs/active/product").glob("*.md") if p.name != "README.md"]


def _active_uat_docs() -> list[Path]:
    return [p for p in (ROOT / "docs/active/uat").glob("*.md") if p.name != "README.md"]


def test_governance_constitution_files_exist() -> None:
    for rel in GOVERNANCE_FILES + SSOT_FILES:
        assert (ROOT / rel).is_file(), rel


def test_archive_readme_exists() -> None:
    text = (ROOT / "docs/archive/README.md").read_text(encoding="utf-8")
    assert "historical" in text.lower()
    assert "never" in text.lower()


def test_active_product_doc_count_within_limit() -> None:
    docs = _active_product_docs()
    assert len(docs) < ACTIVE_PRODUCT_MAX, [p.name for p in docs]


def test_active_uat_doc_count_within_limit() -> None:
    docs = _active_uat_docs()
    assert len(docs) < ACTIVE_UAT_MAX, [p.name for p in docs]


def test_product_master_official_identity_and_flow() -> None:
    text = (ROOT / "docs/active/product/PRODUCT_MASTER.md").read_text(encoding="utf-8")
    assert "social signal intelligence" in text.lower()
    assert "/profile" in text and "/match" in text


def test_active_docs_do_not_link_archive_as_authority() -> None:
    archive_link = re.compile(r"\]\([^)]*docs/archive/[^)]+\)", re.I)
    for path in _active_product_docs() + _active_uat_docs():
        hits = archive_link.findall(path.read_text(encoding="utf-8"))
        assert not hits, f"{path.name} links archive: {hits[:3]}"


def test_ai_constitution_lists_ssot_only() -> None:
    text = (ROOT / "docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md").read_text(encoding="utf-8")
    assert "PRODUCT_MASTER.md" in text
    assert "docs/active/" in text
