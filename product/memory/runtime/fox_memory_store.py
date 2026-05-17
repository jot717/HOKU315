from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, List

from product.persistence.runtime.entities import FOX_MEMORY
from product.persistence.runtime.registry import get_backend
from product.persistence.runtime.schema import SCHEMA_VERSION, with_schema_version

DEFAULT_MEMORY: Dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "recent_patterns": [],
    "recent_warnings": [],
    "last_guardian_note": "",
    "last_seen_energy": "",
    "updated_at": "",
}

_MEMORY_KEYS = frozenset(
    {
        "schema_version",
        "recent_patterns",
        "recent_warnings",
        "last_guardian_note",
        "last_seen_energy",
        "updated_at",
    }
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _string_list(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []
    return [str(x).strip() for x in value if str(x).strip()]


def normalize_fox_memory(raw: Dict[str, Any]) -> Dict[str, Any]:
    merged = deepcopy(DEFAULT_MEMORY)
    if isinstance(raw, dict):
        merged.update({k: v for k, v in raw.items() if k in _MEMORY_KEYS})
    merged["recent_patterns"] = _string_list(merged.get("recent_patterns"))
    merged["recent_warnings"] = _string_list(merged.get("recent_warnings"))
    merged["last_guardian_note"] = str(merged.get("last_guardian_note", "") or "")[:2000]
    merged["last_seen_energy"] = str(merged.get("last_seen_energy", "") or "")[:200]
    merged["updated_at"] = str(merged.get("updated_at", "") or "")
    return with_schema_version(merged)


def load_fox_memory() -> Dict[str, Any]:
    data = get_backend().read(FOX_MEMORY)
    if data is None or not isinstance(data, dict):
        save_fox_memory(dict(DEFAULT_MEMORY))
        return normalize_fox_memory(dict(DEFAULT_MEMORY))
    return normalize_fox_memory(data)


def save_fox_memory(data: Dict[str, Any]) -> None:
    payload = normalize_fox_memory(data if isinstance(data, dict) else {})
    get_backend().write(FOX_MEMORY, payload)


def derive_recurring_note(
    patterns: List[str],
    warnings: List[str],
) -> str:
    """Rule-based companion line from recent tags (no LLM)."""
    if len(warnings) >= 3:
        return "最近讓你疲憊的互動似乎變少了。"
    if len(patterns) >= 3:
        return "你開始照顧自己的節奏，北極狐都看在眼裡。"
    if patterns and warnings:
        return "我會繼續替你留意附近的訊號。"
    if patterns:
        return "我會繼續替你留意附近的訊號。"
    return "多觀察幾次，北極狐就能替你收斂長一點的記憶。"


def get_memory_display() -> Dict[str, str]:
    data = load_fox_memory()
    patterns = [str(x) for x in data.get("recent_patterns", []) if x]
    warnings = [str(x) for x in data.get("recent_warnings", []) if x]
    note = str(data.get("last_guardian_note", "") or "")
    recurring = derive_recurring_note(patterns, warnings)
    if note and recurring == "多觀察幾次，北極狐就能替你收斂長一點的記憶。":
        recurring = "這條守護線，北極狐會替你慢慢收攏。"
    return {
        "guardian_memory_note": note,
        "recurring_pattern": recurring,
    }
