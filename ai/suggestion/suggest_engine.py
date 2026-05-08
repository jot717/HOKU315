"""
Suggest fixes from `ai/taxonomy/error_taxonomy.yaml` (no LLM; deterministic).

Used by `ai.self_heal.suggest_bridge`.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def suggest_fix(error_type: str, taxonomy_path: Path | None = None) -> dict[str, Any]:
    if yaml is None:
        return {"error_type": error_type, "suggestions": [], "error": "PyYAML not installed"}

    root = repo_root()
    path = taxonomy_path or (root / "ai" / "taxonomy" / "error_taxonomy.yaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"error_type": error_type, "suggestions": []}

    entry = data.get(error_type)
    if not isinstance(entry, dict):
        return {"error_type": error_type, "suggestions": []}

    actions = entry.get("suggested_actions") or []
    symptoms = entry.get("symptoms") or []
    causes = entry.get("common_causes") or []

    suggestions: list[dict[str, str]] = []
    if isinstance(actions, list):
        for a in actions[:8]:
            if isinstance(a, str):
                suggestions.append({"fix": a})

    return {
        "error_type": error_type,
        "severity": entry.get("severity"),
        "symptoms_preview": symptoms[:3] if isinstance(symptoms, list) else [],
        "common_causes_preview": causes[:3] if isinstance(causes, list) else [],
        "suggestions": suggestions,
    }


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: python -m ai.suggestion.suggest_engine STATE_DESYNC", file=sys.stderr)
        raise SystemExit(2)
    import json

    print(json.dumps(suggest_fix(sys.argv[1]), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
