from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, MutableMapping

TARGET_PATH = Path("runtime_state/target_profile.json")

DEFAULT_TARGET: Dict[str, Any] = {
    "target_name": "",
    "relationship_type": "",
    "observed_traits": [],
    "communication_style": [],
    "social_patterns": [],
    "pressure_signals": [],
    "instability_level": 0,
    "attention_demand": 0,
    "response_consistency": 5,
    "notes": "",
}


def _ensure_lists(data: MutableMapping[str, Any]) -> None:
    for key in (
        "observed_traits",
        "communication_style",
        "social_patterns",
        "pressure_signals",
    ):
        v = data.get(key)
        if v is None:
            data[key] = []
        elif isinstance(v, str):
            data[key] = [x.strip() for x in v.split(",") if x.strip()]
        elif isinstance(v, list):
            data[key] = [str(x).strip() for x in v if str(x).strip()]
        else:
            data[key] = []


def _coerce_sliders(data: MutableMapping[str, Any]) -> None:
    for key in ("instability_level", "attention_demand", "response_consistency"):
        try:
            n = int(round(float(data.get(key, 0))))
        except (TypeError, ValueError):
            n = 0
        data[key] = max(0, min(10, n))


def normalize_target_profile(raw: Dict[str, Any]) -> Dict[str, Any]:
    merged = deepcopy(DEFAULT_TARGET)
    merged.update({k: v for k, v in raw.items() if k in DEFAULT_TARGET})
    _ensure_lists(merged)
    _coerce_sliders(merged)
    merged["target_name"] = str(merged.get("target_name", "")).strip()[:80]
    merged["relationship_type"] = str(merged.get("relationship_type", "")).strip()[:40]
    merged["notes"] = str(merged.get("notes", "")).strip()[:2000]
    return merged


def save_target_profile(profile: Dict[str, Any]) -> None:
    clean = normalize_target_profile(profile)
    TARGET_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TARGET_PATH, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2, ensure_ascii=False)


def load_target_profile() -> Dict[str, Any]:
    if not TARGET_PATH.exists():
        save_target_profile(DEFAULT_TARGET)
    with open(TARGET_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        raw = {}
    return normalize_target_profile(raw)


def parse_comma_list(text: str) -> List[str]:
    return [x.strip() for x in (text or "").split(",") if x.strip()]
