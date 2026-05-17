#!/usr/bin/env python3
"""
Minimal flow gate: verify backlog + sprint spec files exist for a feature ID.

Convention (this repo):
  backlog/BACKLOG_<FEATURE>.md
  backlog/SPRINT_<FEATURE>.md

Does NOT verify IMPLEMENT / REGRESSION / DONE — see EXECUTION_GATE.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def check_flow(feature: str) -> int:
    root = repo_root()
    fid = feature.strip().upper().replace(" ", "_")
    backlog = root / "backlog" / f"BACKLOG_{fid}.md"
    sprint = root / "backlog" / f"SPRINT_{fid}.md"

    missing: list[str] = []
    if not backlog.is_file():
        missing.append(str(backlog.relative_to(root)))
    if not sprint.is_file():
        missing.append(str(sprint.relative_to(root)))

    if missing:
        for m in missing:
            print(f"MISSING: {m}", file=sys.stderr)
        print("GATE FAILED — BACKLOG or SPRINT spec not found", file=sys.stderr)
        return 1

    print("GATE PASSED (backlog + sprint specs present)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Check BACKLOG/SPRINT spec files for a feature ID.")
    p.add_argument(
        "--feature",
        "-f",
        default="MATCH_FLOW_v1",
        help="Feature ID, e.g. MATCH_FLOW_v1 → BACKLOG_MATCH_FLOW_v1.md",
    )
    args = p.parse_args()
    return check_flow(args.feature)


if __name__ == "__main__":
    raise SystemExit(main())
