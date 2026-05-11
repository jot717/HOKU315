from __future__ import annotations

from typing import Any, Dict

from product.memory.runtime.fox_memory_store import (
    derive_recurring_note,
    load_fox_memory,
    save_fox_memory,
    _utc_now_iso,
)


def remember_insight(insight: Dict[str, Any], score: float) -> Dict[str, str]:
    """
    Rule-based guardian memory update (SAFE MODE).
    low score: remember warning / pressure-avoidance tone
    medium: unstable rhythm
    high: calm signal band
    """
    _ = insight  # reserved for trait-aware rules later
    data = load_fox_memory()
    patterns: list[str] = [str(x) for x in data.get("recent_patterns", [])]
    warnings: list[str] = [str(x) for x in data.get("recent_warnings", [])]

    if score < 60.0:
        tag = "pressure_pause"
        warnings.append(tag)
        patterns.append("常在高壓訊號前停留")
        guardian = "我記得你最近常避開高壓訊號。"
        band = "alert_band"
    elif score < 80.0:
        patterns.append("節奏仍在搖擺觀察")
        guardian = "你最近在比較搖擺的節奏裡觀察訊號。"
        band = "mixed_band"
    else:
        patterns.append("偏向安靜的訊號場")
        guardian = "你開始靠近比較安靜的節奏。"
        band = "calm_band"

    patterns = patterns[-8:]
    warnings = warnings[-8:]

    recurring = derive_recurring_note(patterns, warnings)
    if score >= 80.0 and len(warnings) >= 2:
        recurring = "最近讓你疲憊的互動似乎變少了。"

    data["recent_patterns"] = patterns
    data["recent_warnings"] = warnings
    data["last_guardian_note"] = guardian
    data["last_seen_energy"] = band
    data["updated_at"] = _utc_now_iso()
    save_fox_memory(data)

    return {
        "guardian_memory_note": guardian,
        "recurring_pattern": recurring,
    }
