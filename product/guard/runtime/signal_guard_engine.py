from __future__ import annotations

from typing import Any, Dict, List

from product.memory.runtime.fox_memory_store import load_fox_memory


def evaluate_signal_risk(insight: Dict[str, Any], score: float) -> Dict[str, Any]:
    """Rule-based signal guard; no LLM, no external service."""
    flags: List[str] = []
    risk_level = "low"
    guardian_action = "保持觀察，維持現在的保護距離。"
    guardian_warning = "目前沒有明顯危險。這是一段相對平穩的訊號。"

    activity = str(insight.get("activity_analysis", "") or "")
    traits = insight.get("shared_traits", [])
    trait_count = len(traits) if isinstance(traits, list) else 0

    memory = load_fox_memory()
    recent_patterns = [str(x) for x in memory.get("recent_patterns", [])]
    recent_warnings = [str(x) for x in memory.get("recent_warnings", [])]
    repeated_instability = sum("搖擺" in x for x in recent_patterns) >= 2
    repeated_pressure = len(recent_warnings) >= 2

    if score < 40:
        flags.extend(["高壓節奏", "消耗傾向"])
    if repeated_instability:
        flags.append("訊號不穩定")
    if repeated_pressure:
        flags.append("過度比較")
    if "tension" in activity.lower() or "拉扯" in activity:
        flags.append("節奏失衡")
    if trait_count <= 1:
        flags.append("低共鳴")

    if score >= 75 and not flags:
        flags.append("安全節奏")
    elif score >= 65 and "低共鳴" not in flags and "節奏失衡" not in flags:
        flags.append("平穩觀察")

    high_conditions = score < 40 or repeated_pressure or (
        repeated_instability and "節奏失衡" in flags
    )
    medium_conditions = (
        score < 65
        or repeated_instability
        or "低共鳴" in flags
        or "節奏失衡" in flags
    )

    if high_conditions:
        risk_level = "high"
        guardian_action = "先拉開距離，讓北極狐替你繼續擋掉雜訊。"
        guardian_warning = "我不建議你現在太靠近這個訊號。這裡有些會消耗你的痕跡。"
    elif medium_conditions:
        risk_level = "medium"
        guardian_action = "保持邊界再觀察，先不要急著靠近。"
        guardian_warning = "可以再觀察一下。節奏還不夠穩定。"

    dedup_flags: List[str] = []
    for f in flags:
        if f not in dedup_flags:
            dedup_flags.append(f)

    return {
        "risk_level": risk_level,
        "risk_flags": dedup_flags,
        "guardian_action": guardian_action,
        "guardian_warning": guardian_warning,
    }
