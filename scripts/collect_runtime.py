#!/usr/bin/env python3
"""
Collect backend-oriented runtime snapshot into an incident folder (skeleton).

Does not call Supabase or alter DB. Writes structured files under
debug_evidence/YYYY-MM-DD-slug/.

Usage:
  python scripts/collect_runtime.py my-slug
  python scripts/collect_runtime.py my-slug --date 2026-05-11
  python scripts/collect_runtime.py my-slug --traceback-file path/to/log.txt
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import sys
from datetime import date, datetime
from pathlib import Path

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

REDACT_SUBSTRINGS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PRIVATE", "AUTH", "CREDENTIAL")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def validate_slug(slug: str) -> str:
    slug = slug.strip().lower()
    if not slug or len(slug) > 120:
        sys.exit("error: slug must be non-empty and <= 120 chars")
    if not SLUG_PATTERN.match(slug):
        sys.exit("error: invalid slug (use lowercase letters, numbers, hyphens)")
    return slug


def parse_folder_date(s: str) -> date:
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        sys.exit("error: --date must be YYYY-MM-DD")


def should_redact_key(key: str) -> bool:
    k = key.upper()
    return any(s in k for s in REDACT_SUBSTRINGS)


def redacted_environ() -> dict[str, str]:
    out: dict[str, str] = {}
    for k, v in os.environ.items():
        if should_redact_key(k):
            out[k] = "***REDACTED***"
        else:
            out[k] = v
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect runtime info into debug_evidence (skeleton).")
    parser.add_argument("slug", help="Incident slug, e.g. match-fail")
    parser.add_argument("--date", metavar="YYYY-MM-DD", help="Folder date prefix (default: today)")
    parser.add_argument("--traceback-file", type=Path, help="Optional file to copy into incident as traceback_snippet.txt")
    parser.add_argument("--vector-file", type=Path, help="Optional JSON/text to copy as vector_payload.json")
    parser.add_argument("--rpc-file", type=Path, help="Optional JSON/text to copy as rpc_payload.json")
    args = parser.parse_args()

    slug = validate_slug(args.slug)
    d = parse_folder_date(args.date) if args.date else date.today()
    root = repo_root()
    target = root / "debug_evidence" / f"{d.isoformat()}-{slug}"
    target.mkdir(parents=True, exist_ok=True)

    snapshot = {
        "collected_at": datetime.now().astimezone().isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "cwd": str(Path.cwd()),
        "executable": sys.executable,
        "collector": "collect_runtime.py v1 skeleton",
    }
    (target / "runtime_collect.json").write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    env_path = target / "env_redacted.json"
    env_path.write_text(json.dumps(redacted_environ(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    note = (
        "# Vector / RPC payloads\n\n"
        "Paste or use --vector-file / --rpc-file on next collect run.\n"
        "Manual: copy from DevTools Network into network.json (see debug_evidence/README.md).\n"
    )
    vp = target / "vector_payload.json"
    rp = target / "rpc_payload.json"
    if not vp.exists():
        vp.write_text('{\n  "_note": "skeleton placeholder — replace with real DEBUG_VECTOR / client payload"\n}\n', encoding="utf-8")
    if not rp.exists():
        rp.write_text('{\n  "_note": "skeleton placeholder — replace with PostgREST RPC request body"\n}\n', encoding="utf-8")

    if args.vector_file and args.vector_file.is_file():
        vp.write_text(args.vector_file.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    if args.rpc_file and args.rpc_file.is_file():
        rp.write_text(args.rpc_file.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")

    tb_out = target / "traceback_snippet.txt"
    if args.traceback_file and args.traceback_file.is_file():
        tb_out.write_text(args.traceback_file.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    elif not tb_out.exists():
        tb_out.write_text(
            "# Paste Python traceback from reflex run / backend.txt\n\n",
            encoding="utf-8",
        )

    print(f"Wrote runtime snapshot under {target.relative_to(root)}")


if __name__ == "__main__":
    main()
