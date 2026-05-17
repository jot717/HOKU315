#!/usr/bin/env python3
"""Light guard: BACKLOG.md and SPRINT_LOG.md exist at repo root (cwd-independent)."""

from __future__ import annotations

import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def main() -> int:
    root = repo_root()
    if not (root / "BACKLOG.md").is_file():
        print("NO BACKLOG FOUND — STOP", file=sys.stderr)
        return 1
    if not (root / "SPRINT_LOG.md").is_file():
        print("NO SPRINT LOG FOUND — STOP", file=sys.stderr)
        return 1
    print("PROCESS OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
