#!/usr/bin/env python3
"""
Mock incident replay (v1 skeleton).

Reads files from a debug_evidence incident folder and prints what a real replay
would do - without calling PostgREST, mutating DB, or loading full app state.

Usage:
  python -m ai.replay.replay_incident --incident debug_evidence/2026-05-11-example
  python -m ai.replay.replay_incident debug_evidence/2026-05-11-example   # v1-lite positional
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def load_json(path: Path) -> object | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"_parse_error": str(path)}


def mock_replay_state(incident: Path) -> dict[str, object]:
    """Placeholder: real implementation would deserialize Reflex state snapshots."""
    snap = incident / "state_snapshot.json"
    if snap.is_file():
        return {"source": str(snap), "mode": "file_present", "mock": True}
    return {"source": None, "mode": "no_snapshot", "mock": True}


def main() -> None:
    root = repo_root()
    p = argparse.ArgumentParser(description="Mock replay for HOKU315 incidents (skeleton).")
    p.add_argument(
        "--incident",
        "-i",
        type=Path,
        default=None,
        help="Path to debug_evidence/YYYY-MM-DD-slug/",
    )
    p.add_argument(
        "incident_positional",
        nargs="?",
        type=Path,
        default=None,
        help="(v1-lite) same as --incident",
    )
    args = p.parse_args()
    raw = args.incident or args.incident_positional
    if raw is None:
        p.error(
            "pass incident folder: python -m ai.replay.replay_incident debug_evidence/YYYY-MM-DD-slug "
            "or --incident ..."
        )
    incident = raw.resolve()
    if not incident.is_dir():
        sys.exit(f"error: not a directory: {incident}")

    print("=== MOCK REPLAY (no side effects) ===")
    print(f"incident: {incident.relative_to(root)}")
    print()

    runtime_lite = load_json(incident / "runtime.json")
    print("[0] runtime.json (v1-lite observation bundle)")
    if runtime_lite and isinstance(runtime_lite, dict):
        print(f"  loaded snapshot keys: {list(runtime_lite.keys())}")
    else:
        print("  (optional) missing or invalid; run scripts/collect_runtime.py <slug>")
    print()

    rpc = load_json(incident / "rpc_payload.json")
    vec = load_json(incident / "vector_payload.json")
    net = load_json(incident / "network.json")

    print("[1] RPC payload (rpc_payload.json or network-derived)")
    if rpc:
        print(f"  would invoke RPC with keys: {list(rpc.keys()) if isinstance(rpc, dict) else type(rpc)}")
    else:
        print("  (none) - fill rpc_payload.json or network.json")
    print()

    print("[2] Vector payload")
    if vec:
        print(f"  would validate vector payload type={type(vec).__name__}")
    else:
        print("  (none)")
    print()

    print("[3] Network snapshot")
    if net:
        print("  would replay HTTP layer from network.json (DevTools export)")
    else:
        print("  (optional) network.json missing")
    print()

    print("[4] State snapshot")
    print(f"  {mock_replay_state(incident)}")
    print()
    print("See docs/REPLAY_GUIDE.md for the full replay pipeline.")


if __name__ == "__main__":
    main()
