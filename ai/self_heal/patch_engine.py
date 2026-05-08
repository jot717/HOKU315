#!/usr/bin/env python3
"""Generate pending-review patch JSON under ai/self_heal/patches/."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def safe_slug(error_type: str) -> str:
    s = error_type.strip().upper().replace(" ", "_")
    s = re.sub(r"[^A-Z0-9_-]+", "_", s)
    return s or "UNKNOWN"


def generate_patch(error_type: str, suggestion: str) -> Path:
    patch = {
        "error_type": error_type,
        "suggestion": suggestion,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pending_review",
    }

    root = repo_root()
    patches_dir = root / "ai" / "self_heal" / "patches"
    patches_dir.mkdir(parents=True, exist_ok=True)

    path = patches_dir / f"{safe_slug(error_type)}.json"
    path.write_text(json.dumps(patch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("PATCH GENERATED:", path.relative_to(root))
    return path


def main() -> None:
    p = argparse.ArgumentParser(description="Write pending patch JSON (review-only workflow).")
    p.add_argument("error_type", help="e.g. STATE_DESYNC")
    p.add_argument(
        "suggestion",
        nargs="?",
        default=None,
        help="Suggestion text; omit to pull first taxonomy suggested_actions via suggest_engine",
    )
    args = p.parse_args()

    suggestion = args.suggestion
    if suggestion is None:
        from ai.suggestion.suggest_engine import suggest_fix

        res = suggest_fix(args.error_type)
        sugs = res.get("suggestions") if isinstance(res, dict) else None
        if isinstance(sugs, list) and sugs and isinstance(sugs[0], dict):
            suggestion = str(sugs[0].get("fix") or "").strip()
        if not suggestion:
            sys.exit("error: no taxonomy suggestion for this error_type; pass suggestion explicitly")

    generate_patch(args.error_type, suggestion)


if __name__ == "__main__":
    main()
