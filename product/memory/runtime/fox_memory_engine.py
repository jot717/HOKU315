from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence

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


def record_relationship_simulation_memory(
    archetype_name: str,
    interaction_risk_score: int,
) -> None:
    """Tag recurring interaction-pattern exposure (SAFE MODE, synthetic archetype)."""
    if interaction_risk_score < 42:
        return
    data = load_fox_memory()
    patterns: list[str] = [str(x) for x in data.get("recent_patterns", [])]
    short = (archetype_name or "").strip()[:24] or "示範原型"
    tag = f"互動警示：{short}（壓力偏高）"
    if tag not in patterns:
        patterns.append(tag)
    patterns = patterns[-10:]
    data["recent_patterns"] = patterns
    data["updated_at"] = _utc_now_iso()
    save_fox_memory(data)


def record_target_pattern_memory(
    target_name: str,
    archetype_name: str,
    interaction_risk_score: int,
) -> None:
    """Tag recurring target × interaction pattern exposure (SAFE MODE)."""
    name = (target_name or "").strip()
    if not name or interaction_risk_score < 46:
        return
    short_t = name[:12]
    short_a = (archetype_name or "").strip()[:18] or "互動模式"
    tag = f"目標壓力重複：{short_t}×{short_a}"
    data = load_fox_memory()
    patterns: list[str] = [str(x) for x in data.get("recent_patterns", [])]
    if tag not in patterns:
        patterns.append(tag)
    patterns = patterns[-10:]
    data["recent_patterns"] = patterns
    data["updated_at"] = _utc_now_iso()
    save_fox_memory(data)


def apply_inference_memory_tags(
    risk_scores: Mapping[str, float],
    risk_types: Sequence[str],
) -> None:
    """
    Append short rule-based tags when inferred risks are elevated (SAFE MODE).
    Called after remember_insight so score-based memory is already written.
    """
    data = load_fox_memory()
    patterns: list[str] = [str(x) for x in data.get("recent_patterns", [])]

    tags: list[str] = []
    for key in risk_types[:4]:
        val = float(risk_scores.get(key, 0.0))
        if val < 0.52:
            continue
        if key == "manipulation_sensitivity":
            tags.append("推論：操弄壓力訊號偏高")
        elif key == "attention_drain_risk":
            tags.append("推論：注意力消耗偏高")
        elif key == "ghosting_sensitivity":
            tags.append("推論：回覆節奏壓力偏高")
        elif key == "emotional_exhaustion_risk":
            tags.append("推論：疲勞堆疊訊號偏高")
        elif key == "social_comparison_risk":
            tags.append("推論：比較壓力偏高")
        if len(tags) >= 2:
            break

    for t in tags:
        if t not in patterns:
            patterns.append(t)
    patterns = patterns[-10:]
    data["recent_patterns"] = patterns
    data["updated_at"] = _utc_now_iso()
    save_fox_memory(data)

