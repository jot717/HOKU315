from __future__ import annotations

import inspect
from pathlib import Path

from fox_quiz.login_page import login_page
from fox_quiz.ui.pages.home_page import home_page

ROOT = Path(__file__).resolve().parents[2]


def test_product_master_exists() -> None:
    p = ROOT / "docs/active/product/PRODUCT_MASTER.md"
    text = p.read_text(encoding="utf-8")
    assert p.is_file()
    assert "Guest" in text or "訪客" in text
    assert "PRODUCT_MASTER" in text or "Single Source" in text
    assert "SIGNAL_SYSTEM.md" in text or "social signal" in text.lower()


def test_master_backlog_exists() -> None:
    p = ROOT / "docs/active/governance/MASTER_BACKLOG.md"
    text = p.read_text(encoding="utf-8")
    assert "ACTIVE" in text
    assert "COMPLETED" in text


def test_uat_master_guide_exists() -> None:
    assert (ROOT / "docs/active/uat/UAT_MASTER_GUIDE.md").is_file()


def test_readme_indexes_exist() -> None:
    for rel in (
        "docs/active/product/README.md",
        "docs/active/uat/README.md",
        "backlog/README.md",
    ):
        assert (ROOT / rel).is_file(), rel


def test_deprecated_archive_exists() -> None:
    assert (ROOT / "docs/deprecated/archive/README.md").is_file()
    assert (ROOT / "docs/archive/legacy").is_dir()
    assert (ROOT / "backlog/archive").is_dir()


def test_repo_governance_rules_exist() -> None:
    text = (ROOT / "docs/active/governance/REPO_GOVERNANCE_RULES.md").read_text(encoding="utf-8")
    assert "PRODUCT_MASTER" in text
    assert "forbidden" in text.lower() or "parallel" in text.lower()


def test_home_guest_and_account_copy() -> None:
    src = inspect.getsource(home_page)
    assert "立即開始分析" in src
    assert "登入以保存長期互動趨勢" in src
    assert "訪客" in src


def test_login_guest_clarity() -> None:
    src = inspect.getsource(login_page)
    assert "訪客" in src
    assert "帳號" in src


def test_core_ssot_docs_not_deleted() -> None:
    for rel in (
        "docs/active/product/SIGNAL_SYSTEM.md",
        "docs/active/product/MATCH_SYSTEM.md",
        "docs/active/product/ROADMAP.md",
        "docs/active/governance/DEVELOPMENT_CONSTITUTION.md",
    ):
        assert (ROOT / rel).is_file(), rel


def test_pages_compile() -> None:
    assert home_page() is not None
    assert login_page() is not None
