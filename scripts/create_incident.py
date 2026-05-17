#!/usr/bin/env python3
"""Create standardized debug_evidence/YYYY-MM-DD-slug/ incident folder."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

ROOT_CAUSE_MD = """# Root Cause

## 問題

描述現象

## 根因

真正原因

## 修正

修了什麼

## 驗證

如何確認修復成功

## 影響範圍

哪些功能受影響
"""

CONSOLE_TXT = """# Browser Console — paste full errors / warnings below (see ops/debug/DEBUG_GUIDE.md §6)


"""

NETWORK_JSON = """{
  "_instructions": "Paste RPC requests/responses from DevTools Network (filter: rpc). Remove secrets.",
  "entries": []
}
"""

BACKEND_TXT = """# reflex run terminal — paste traceback / DEBUG_VECTOR / errors below (see ops/debug/DEBUG_GUIDE.md §6)


"""

RPC_SQL = """-- Supabase SQL Editor — reproduction / deploy / verify (see sql/match_logic.sql, sql/DEPLOY_LOG.md)


"""

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Create debug_evidence incident template folder.")
    p.add_argument("slug", help="Short slug, e.g. match-fail")
    p.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        help="Folder date prefix (default: today).",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Remove existing folder if present (dangerous).",
    )
    return p.parse_args()


def validate_slug(slug: str) -> str:
    slug = slug.strip().lower()
    if not slug or len(slug) > 120:
        sys.exit("error: slug must be non-empty and <= 120 chars")
    if not SLUG_PATTERN.match(slug):
        sys.exit(
            "error: slug must be lowercase alphanumeric segments separated by hyphens "
            "(e.g. match-fail, rpc-pgrst205)"
        )
    return slug


def parse_folder_date(s: str) -> date:
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        sys.exit("error: --date must be YYYY-MM-DD")


def main() -> None:
    args = parse_args()
    slug = validate_slug(args.slug)
    d = parse_folder_date(args.date) if args.date else date.today()
    day_str = d.isoformat()
    root = repo_root()
    ev = root / "debug_evidence"
    target = ev / f"{day_str}-{slug}"

    if target.exists():
        if not args.force:
            rel = target.relative_to(root)
            sys.exit(
                f"error: folder already exists: {rel}\n"
                "  Use --force to replace it."
            )
        shutil.rmtree(target)

    ev.mkdir(parents=True, exist_ok=True)
    target.mkdir(parents=False)

    (target / "console.txt").write_text(CONSOLE_TXT, encoding="utf-8")
    (target / "network.json").write_text(NETWORK_JSON, encoding="utf-8")
    (target / "backend.txt").write_text(BACKEND_TXT, encoding="utf-8")
    (target / "rpc.sql").write_text(RPC_SQL, encoding="utf-8")
    (target / "root_cause.md").write_text(ROOT_CAUSE_MD, encoding="utf-8")

    print(f"Created {target.relative_to(root)}")


if __name__ == "__main__":
    main()
