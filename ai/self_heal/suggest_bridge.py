#!/usr/bin/env python3
"""Taxonomy suggestion -> pending patch JSON (manual review required)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ai.self_heal.patch_engine import generate_patch
from ai.suggestion.suggest_engine import suggest_fix


def run(error_type: str) -> Path | None:
    result = suggest_fix(error_type)
    suggestions = result.get("suggestions") if isinstance(result, dict) else None

    if isinstance(suggestions, list) and suggestions:
        first = suggestions[0]
        if isinstance(first, dict) and "fix" in first:
            return generate_patch(error_type, str(first["fix"]))

    print("No suggestions for error_type:", error_type, file=sys.stderr)
    return None


def main() -> None:
    p = argparse.ArgumentParser(description="Suggest from taxonomy and write patch JSON.")
    p.add_argument("error_type", help="e.g. STATE_DESYNC")
    args = p.parse_args()
    path = run(args.error_type.strip())
    if path is None:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
