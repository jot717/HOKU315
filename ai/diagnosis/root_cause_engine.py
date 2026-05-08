#!/usr/bin/env python3
"""
Skeleton root-cause classifier: reads debug_evidence incident folders + taxonomy YAML.

CLI:
  python -m ai.diagnosis.root_cause_engine --incident debug_evidence/2026-05-11-example
  python -m ai.diagnosis.root_cause_engine --scan-latest
  python -m ai.diagnosis.root_cause_engine --error-type STATE_DESYNC   # v1-lite taxonomy lookup
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def load_taxonomy(path: Path) -> dict[str, Any]:
    if yaml is None:
        sys.exit("error: install PyYAML (pip install PyYAML) to load error_taxonomy.yaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        sys.exit(f"error: invalid taxonomy YAML: {path}")
    return data


def incident_text_bundle(incident_dir: Path) -> str:
    parts: list[str] = []
    for name in ("console.txt", "backend.txt", "root_cause.md", "rpc.sql"):
        fp = incident_dir / name
        if fp.is_file():
            parts.append(fp.read_text(encoding="utf-8", errors="replace"))
    nj = incident_dir / "network.json"
    if nj.is_file():
        parts.append(nj.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts).lower()


def score_keyword(text: str, keywords: tuple[str, ...]) -> int:
    return sum(1 for kw in keywords if kw in text)


def classify(text: str, taxonomy: dict[str, Any]) -> list[tuple[str, int, dict[str, Any]]]:
    """Return list of (type_name, score, entry) sorted by score descending."""
    keyword_map: dict[str, tuple[str, ...]] = {
        "VECTOR_FORMAT_ERROR": ("malformed array", "vector", "pgvector", "literal", "::vector"),
        "RPC_SIGNATURE_ERROR": ("pgrst", "rpc", "postgrest", "function", "signature", "not found"),
        "HYDRATION_ERROR": ("hydration", "<p>", "descendant", "ssr", "react"),
        "STATE_DESYNC": ("immutablestate", "state", "reflex", "background"),
        "ASYNC_RUNTIME_ERROR": ("asyncio", "coroutine", "await", "event loop", "runtimeerror"),
    }
    results: list[tuple[str, int, dict[str, Any]]] = []
    for key, entry in taxonomy.items():
        if not isinstance(entry, dict) or key.startswith("_"):
            continue
        kws = keyword_map.get(key, ())
        s = score_keyword(text, kws)
        results.append((key, s, entry))
    results.sort(key=lambda x: (-x[1], x[0]))
    return results


def find_latest_incident(evidence_root: Path) -> Path | None:
    dirs = [p for p in evidence_root.iterdir() if p.is_dir() and re.match(r"^\d{4}-\d{2}-\d{2}-", p.name)]
    if not dirs:
        return None
    return max(dirs, key=lambda p: p.name)


def suggest_root_cause(incident_dir: Path, taxonomy_path: Path) -> str:
    taxonomy = load_taxonomy(taxonomy_path)
    blob = incident_text_bundle(incident_dir)
    ranked = classify(blob, taxonomy)
    lines = [
        f"# Root cause suggestion (skeleton)",
        "",
        f"**Incident**: `{incident_dir.relative_to(repo_root())}`",
        "",
        "## Ranked incident types",
        "",
    ]
    for name, score, entry in ranked:
        lines.append(f"### {name} (score={score})")
        lines.append(f"- **severity**: {entry.get('severity', 'n/a')}")
        causes = entry.get("common_causes") or []
        if isinstance(causes, list):
            lines.append("- **common_causes**:")
            for c in causes[:5]:
                lines.append(f"  - {c}")
        actions = entry.get("suggested_actions") or []
        if isinstance(actions, list):
            lines.append("- **suggested_actions**:")
            for a in actions[:5]:
                lines.append(f"  - {a}")
        lines.append("")
    top = ranked[0][0] if ranked else "UNKNOWN"
    lines.append("## Primary guess")
    lines.append(f"Use **{top}** as starting hypothesis; confirm with human review and replay (see docs/REPLAY_GUIDE.md).")
    lines.append("")
    return "\n".join(lines)


def taxonomy_lookup(error_type: str, taxonomy_path: Path) -> dict[str, Any]:
    taxonomy = load_taxonomy(taxonomy_path)
    entry = taxonomy.get(error_type)
    if isinstance(entry, dict):
        return dict(entry)
    return {"result": "unknown error", "error_type": error_type}


def main() -> None:
    root = repo_root()
    default_tax = root / "ai" / "taxonomy" / "error_taxonomy.yaml"
    parser = argparse.ArgumentParser(description="Classify incident from debug_evidence (skeleton).")
    parser.add_argument("--incident", type=Path, help="Path to debug_evidence/YYYY-MM-DD-slug/")
    parser.add_argument("--scan-latest", action="store_true", help="Pick latest dated folder under debug_evidence/")
    parser.add_argument(
        "--error-type",
        metavar="NAME",
        help="v1-lite: print taxonomy entry for VECTOR_FORMAT_ERROR, RPC_SIGNATURE_ERROR, STATE_DESYNC, ...",
    )
    parser.add_argument("--taxonomy", type=Path, default=default_tax)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable summary to stdout")
    args = parser.parse_args()

    if not args.taxonomy.is_file():
        sys.exit(f"error: missing taxonomy: {args.taxonomy}")

    if args.error_type:
        out = taxonomy_lookup(args.error_type.strip(), args.taxonomy)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    ev = root / "debug_evidence"
    if args.scan_latest:
        inc = find_latest_incident(ev)
        if inc is None:
            sys.exit("error: no debug_evidence subfolders matching YYYY-MM-DD-*")
    elif args.incident:
        inc = args.incident.resolve()
        if not inc.is_dir():
            sys.exit(f"error: not a directory: {inc}")
    else:
        parser.error("provide --incident, --scan-latest, or --error-type")

    if args.json:
        taxonomy = load_taxonomy(args.taxonomy)
        blob = incident_text_bundle(inc)
        ranked = classify(blob, taxonomy)
        out = {
            "incident": str(inc.relative_to(root)),
            "ranked": [{"type": n, "score": s, "severity": t.get("severity")} for n, s, t in ranked],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print(suggest_root_cause(inc, args.taxonomy))


if __name__ == "__main__":
    main()
