from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ACTIVE_PRODUCT_MAX = 10
ACTIVE_UAT_MAX = 5

FORBIDDEN_IN_ACTIVE = (
    "therapy app",
    "emotional healing",
    "compatibility score",
    "personality analyzer",
    "dating score",
    "trauma healing",
)

GOVERNANCE_FILES = (
    "ops/product/AI_DEVELOPMENT_CONSTITUTION.md",
    "ops/product/CANONICAL_TERMINOLOGY.md",
    "ops/product/GOVERNANCE_CHECKLIST.md",
    "ops/product/ACTIVE_SURFACE_MAP.md",
)

SSOT_FILES = (
    "ops/product/PRODUCT_MASTER.md",
    "ops/product/SIGNAL_SYSTEM.md",
    "ops/product/MATCH_SYSTEM.md",
    "ops/product/ROADMAP.md",
)

UAT_AUDIT_EXCLUDE = {
    "DEAD_ROUTE_AUDIT.md",
    "DEAD_COMPONENT_AUDIT.md",
    "PHASE1H3_REPO_MINIMIZATION_REPORT.md",
}


def _active_product_docs() -> list[Path]:
    return [p for p in (ROOT / "ops/product").glob("*.md") if p.name != "README.md"]


def _active_uat_docs() -> list[Path]:
    return [
        p
        for p in (ROOT / "ops/uat").glob("*.md")
        if p.name != "README.md" and p.name not in UAT_AUDIT_EXCLUDE
    ]


def test_governance_constitution_files_exist() -> None:
    for rel in GOVERNANCE_FILES + SSOT_FILES:
        assert (ROOT / rel).is_file(), rel


def test_archive_readme_exists() -> None:
    text = (ROOT / "docs/archive/README.md").read_text(encoding="utf-8")
    assert "historical" in text.lower()
    assert "must not" in text.lower() or "must **not**" in text


def test_active_product_doc_count_within_limit() -> None:
    docs = _active_product_docs()
    assert len(docs) < ACTIVE_PRODUCT_MAX, [p.name for p in docs]


def test_active_uat_doc_count_within_limit() -> None:
    docs = _active_uat_docs()
    assert len(docs) < ACTIVE_UAT_MAX, [p.name for p in docs]


def test_product_master_official_identity_and_flow() -> None:
    text = (ROOT / "ops/product/PRODUCT_MASTER.md").read_text(encoding="utf-8")
    assert "AI social signal intelligence" in text or "social signal intelligence" in text
    assert "dangerous" in text.lower() or "high-drain" in text.lower()
    assert "/profile" in text and "/quiz" in text and "/target" in text
    assert "/insight" in text and "/match" in text
    assert "therapy" in text.lower()  # listed as NOT
    assert "SIGNAL_SYSTEM.md" in text
    assert "MATCH_SYSTEM.md" in text


def test_active_docs_do_not_link_archive_as_authority() -> None:
    archive_link = re.compile(r"\]\([^)]*docs/archive/[^)]+\)", re.I)
    for path in _active_product_docs() + _active_uat_docs():
        text = path.read_text(encoding="utf-8")
        hits = archive_link.findall(text)
        assert not hits, f"{path.name} links archive: {hits[:3]}"


def _line_uses_forbidden_term(line: str, term: str) -> bool:
    lower = line.lower()
    if term not in lower:
        return False
    if "forbidden" in lower or "→ not:" in lower or f"not {term}" in lower:
        return False
    if "| avoid |" in lower or "listed as not" in lower:
        return False
    idx = lower.find(term)
    prefix = lower[max(0, idx - 40) : idx]
    if re.search(r"\bnot\b", prefix):
        return False
    return True


def test_active_docs_avoid_forbidden_terminology() -> None:
    for path in _active_product_docs() + _active_uat_docs():
        if path.name == "CANONICAL_TERMINOLOGY.md":
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            for term in FORBIDDEN_IN_ACTIVE:
                assert not _line_uses_forbidden_term(
                    line, term
                ), f"{path.name} line uses forbidden term {term!r}: {line[:80]}"


def test_ai_constitution_lists_ssot_only() -> None:
    text = (ROOT / "ops/product/AI_DEVELOPMENT_CONSTITUTION.md").read_text(encoding="utf-8")
    assert "PRODUCT_MASTER.md" in text
    assert "SIGNAL_SYSTEM.md" in text
    assert "MATCH_SYSTEM.md" in text
    assert "No second system" in text or "second system" in text.lower()
