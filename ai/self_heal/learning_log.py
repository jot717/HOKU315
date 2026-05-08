#!/usr/bin/env python3
"""Append-only JSON log of fix outcomes (local tooling)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def log_fix(error_type: str, success: bool) -> dict[str, object]:
    log_entry = {
        "error_type": error_type,
        "success": success,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    root = repo_root()
    logs_dir = root / "ai" / "self_heal" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    path = logs_dir / "fix_log.json"

    data: list[object] = []
    if path.is_file():
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(raw, list):
                data = raw
        except json.JSONDecodeError:
            data = []

    data.append(log_entry)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("LOGGED:", log_entry)
    return log_entry


def main() -> None:
    p = argparse.ArgumentParser(description="Append outcome to ai/self_heal/logs/fix_log.json")
    p.add_argument("error_type")
    p.add_argument("--success", action="store_true", help="mark success")
    p.add_argument("--failure", action="store_true", help="mark failure")
    args = p.parse_args()
    if args.success == args.failure:
        sys.exit("error: pass exactly one of --success or --failure")
    log_fix(args.error_type, args.success)


if __name__ == "__main__":
    main()
