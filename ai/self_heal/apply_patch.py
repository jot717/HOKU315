#!/usr/bin/env python3
"""
Review-only: prints patch contents and reminds operator to run regression.

Does NOT modify application source or deploy anything.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def apply_patch(patch_file: Path) -> None:
    patch = json.loads(patch_file.read_text(encoding="utf-8"))

    print("APPLY REVIEW MODE ONLY (no files changed)")
    print("ERROR:", patch.get("error_type"))
    print("SUGGESTION:", patch.get("suggestion"))
    print("STATUS:", patch.get("status"))
    print()
    print("Run regression before applying manually:")
    print("  python scripts/run_regression.py")


def main() -> None:
    root = repo_root()
    default = root / "ai" / "self_heal" / "patches" / "STATE_DESYNC.json"
    p = argparse.ArgumentParser(description="Print patch for human review (safe mode).")
    p.add_argument("--patch", type=Path, default=default, help="Path to patch JSON")
    args = p.parse_args()
    path = args.patch.resolve()
    if not path.is_file():
        sys.exit(f"error: patch file not found: {path}")
    apply_patch(path)


if __name__ == "__main__":
    main()
