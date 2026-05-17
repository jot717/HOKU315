from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from product.persistence.runtime.entities import FOX_MEMORY
from product.persistence.runtime.registry import get_backend

DEFAULT_MEMORY: Dict[str, Any] = {
    "recent_patterns": [],
    "recent_warnings": [],
    "last_guardian_note": "",
    "last_seen_energy": "",
    "updated_at": "",
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_fox_memory() -> Dict[str, Any]:
    data = get_backend().read(FOX_MEMORY)
    if data is None:
        save_fox_memory(dict(DEFAULT_MEMORY))
        data = dict(DEFAULT_MEMORY)
    merged = dict(DEFAULT_MEMORY)
    if isinstance(data, dict):
        merged.update(data)
    return merged


def save_fox_memory(data: Dict[str, Any]) -> None:
    payload = dict(DEFAULT_MEMORY)
    payload.update(data)
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
