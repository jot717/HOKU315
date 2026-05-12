"""
Synthetic relationship archetypes for interaction-risk simulation (SAFE MODE).

No SNS, no multi-user backend, no LLM — rule templates + overlap with user
signal profile (e.g. inference risk_scores).
"""
from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Mapping, MutableMapping, Sequence

# Stable rotation for tests / reproducible demos (not wall-clock random).
def _archetype_index() -> int:
    h = hashlib.sha256(b"RELATIONSHIP_SIGNAL_SIMULATION_v1").hexdigest()
    return int(h[:8], 16) % 7


_ARCHETYPES: tuple[Dict[str, Any], ...] = (
    {
        "archetype_name": "幽靈型互動（示範原型）",
        "interaction_signals": [
            "delayed reassurance",
            "emotional ambiguity",
            "emotional unpredictability",
        ],
        "danger_summary": "回覆忽冷忽熱、需要安撫時長時間缺席，容易讓你的節奏懸在半空。",
        "guardian_warning": "這類互動會讓你反覆猜「是不是我做錯了」，其實是節奏不對等。",
        "risk_pressure": "MEDIUM",
        "_amplify_keys": ("ghosting_sensitivity", "emotional_exhaustion_risk"),
    },
    {
        "archetype_name": "情緒耗能型（示範原型）",
        "interaction_signals": [
            "attention extraction",
            "pressure escalation",
            "validation farming",
        ],
        "danger_summary": "長期要你承接情緒、卻很少對等回饋，像一直在被借電。",
        "guardian_warning": "若對方只在低潮時出現、需要你滿血支援，北極狐會替你盯這條線。",
        "risk_pressure": "HIGH",
        "_amplify_keys": ("attention_drain_risk", "emotional_exhaustion_risk", "approval_dependency_risk"),
    },
    {
        "archetype_name": "被動攻擊型（示範原型）",
        "interaction_signals": [
            "passive hostility",
            "emotional ambiguity",
            "guilt-driven interaction",
        ],
        "danger_summary": "酸話包裝成玩笑、冷處理、讓你猜不透真實態度。",
        "guardian_warning": "這種互動會逼你用大量腦力「讀空氣」，比正面衝突更累。",
        "risk_pressure": "HIGH",
        "_amplify_keys": ("passive_aggression_risk", "manipulation_sensitivity"),
    },
    {
        "archetype_name": "認可收割型（示範原型）",
        "interaction_signals": [
            "validation farming",
            "attention extraction",
            "social comparison pressure",
        ],
        "danger_summary": "用曖昧肯定換你的投入，卻不願意給清楚承諾或對等時間。",
        "guardian_warning": "當讚美像釣鉤、下一步永遠要你證明自己，這是注意力收割。",
        "risk_pressure": "MEDIUM",
        "_amplify_keys": ("approval_dependency_risk", "attention_drain_risk", "social_comparison_risk"),
    },
    {
        "archetype_name": "操弄壓力型（示範原型）",
        "interaction_signals": [
            "guilt-driven interaction",
            "pressure escalation",
            "unstable affection",
        ],
        "danger_summary": "用愧疚、情緒高低起伏讓你難以離場，界線變得模糊。",
        "guardian_warning": "若你常覺得「不配合就對不起對方」，這裡有操弄壓力的影子。",
        "risk_pressure": "HIGH",
        "_amplify_keys": ("manipulation_sensitivity", "unstable_relationship_risk", "emotional_exhaustion_risk"),
    },
    {
        "archetype_name": "混亂社交型（示範原型）",
        "interaction_signals": [
            "emotional unpredictability",
            "pressure escalation",
            "attention extraction",
        ],
        "danger_summary": "能量忽高忽低、計畫常改、讓你難以預期下一步。",
        "guardian_warning": "不可預測的節奏會讓神經系統一直待命，社交疲勞會堆很快。",
        "risk_pressure": "MEDIUM",
        "_amplify_keys": ("emotional_exhaustion_risk", "overexposure_risk", "unsafe_circle_tolerance"),
    },
    {
        "archetype_name": "先甜後壓型（示範原型）",
        "interaction_signals": [
            "unstable affection",
            "attention extraction",
            "emotional ambiguity",
        ],
        "danger_summary": "前期過度親密與保證，後期轉成要求與情緒重量。",
        "guardian_warning": "信任被當成籌碼時，你會先懷疑自己，北極狐會先幫你看互動形狀。",
        "risk_pressure": "HIGH",
        "_amplify_keys": ("manipulation_sensitivity", "unstable_relationship_risk", "attention_drain_risk"),
    },
)


def generate_relationship_archetype() -> Dict[str, Any]:
    """Return one synthetic archetype package (public fields only)."""
    spec = _ARCHETYPES[_archetype_index()]
    return {
        "archetype_name": spec["archetype_name"],
        "interaction_signals": list(spec["interaction_signals"]),
        "danger_summary": spec["danger_summary"],
        "guardian_warning": spec["guardian_warning"],
        "risk_pressure": spec["risk_pressure"],
    }


def _archetype_spec_by_name(zh_name: str) -> Dict[str, Any] | None:
    for s in _ARCHETYPES:
        if s["archetype_name"] == zh_name:
            return s
    return None


def simulate_relationship_risk(
    user_signal_profile: Mapping[str, Any],
    archetype: Mapping[str, Any],
) -> Dict[str, Any]:
    """
    Overlap user inference scores with archetype stressors (rule-based).

    user_signal_profile expects:
      - risk_scores: dict[str, float] (from infer_signal_risks)
      - risk_types: optional list[str]
      - profile: optional dict with activity (1-10)
    """
    risk_scores: MutableMapping[str, float] = dict(
        user_signal_profile.get("risk_scores") or {}
    )
    profile = user_signal_profile.get("profile") or {}
    activity = int(profile.get("activity", 5) or 5)
    activity_n = max(0.0, min(1.0, activity / 10.0))

    name = str(archetype.get("archetype_name", ""))
    spec = _archetype_spec_by_name(name)
    amplify: Sequence[str] = spec["_amplify_keys"] if spec else ()

    raw = 22.0
    matches: List[str] = []
    for key in amplify:
        val = float(risk_scores.get(key, 0.0))
        raw += val * 38.0
        if val >= 0.42:
            matches.append(f"你的「{key}」訊號偏高，容易和「{name}」疊成壓力。")

    raw += activity_n * 12.0
    interaction_risk_score = int(max(0, min(100, round(raw))))

    explanations: List[str] = [
        "這段描述的是「互動形狀」，不是在說你脆弱，也不是在說對方一定是壞人。",
        f"這類互動常見的疲勞點：{archetype.get('danger_summary', '')}",
    ]
    if matches:
        explanations.insert(1, matches[0])
    explanations = [str(x) for x in explanations if str(x).strip()][:3]

    advice = (
        "先保護自己的回覆節奏與睡眠；若對方長期只帶來消耗，北極狐建議你把距離當成工具，不是懲罰。"
        if interaction_risk_score >= 55
        else "維持觀察即可：把互動當成訊號，不急着下結論，也不急着自責。"
    )

    return {
        "interaction_risk_score": interaction_risk_score,
        "risk_matches": matches[:4],
        "danger_explanation": explanations,
        "guardian_advice": advice,
    }
