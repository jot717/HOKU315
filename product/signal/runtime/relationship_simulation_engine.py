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


def _bound_int(value: Any, default: int = 0) -> int:
    try:
        n = int(round(float(value)))
    except (TypeError, ValueError):
        return default
    return max(0, min(10, n))


def _target_keyword_blob(target: Mapping[str, Any]) -> str:
    parts: List[str] = []
    for key in (
        "observed_traits",
        "communication_style",
        "social_patterns",
        "pressure_signals",
        "notes",
        "relationship_type",
    ):
        v = target.get(key)
        if isinstance(v, list):
            parts.extend(str(x) for x in v)
        elif v is not None:
            parts.append(str(v))
    return " ".join(parts).lower()


def archetype_for_target_profile(target: Mapping[str, Any]) -> Dict[str, Any]:
    """Pick synthetic archetype from target text + sliders (rule-based)."""
    blob = _target_keyword_blob(target)
    scores = [0.0] * len(_ARCHETYPES)

    def hit(i: int, w: float, *needles: str) -> None:
        for n in needles:
            if n and n.lower() in blob:
                scores[i] += w

    hit(0, 4.0, "消失", "不回", "ghost", "忽冷忽熱", "已讀不回")
    hit(1, 4.0, "情緒", "低潮", "要你", "討拍", "借電", "drain")
    hit(2, 4.0, "酸", "冷處理", "被動", "passive", "讀空氣")
    hit(3, 4.0, "讚美", "釣", "承諾模糊", "validation", "收割")
    hit(4, 4.0, "愧疚", "操弄", "guilt", "情勒")
    hit(5, 4.0, "亂", "改期", "chaos", "不可預期", "翻臉")
    hit(6, 4.0, "信任", "先甜", "保證", "親密", "籌碼")

    inst = _bound_int(target.get("instability_level"))
    att = _bound_int(target.get("attention_demand"))
    resp = _bound_int(target.get("response_consistency"), 5)

    scores[0] += (10 - resp) * 1.2
    scores[1] += att * 1.4
    scores[4] += inst * 0.9 + att * 0.35
    scores[5] += inst * 1.1
    scores[6] += inst * 0.75 + (10 - resp) * 0.35

    best = max(range(len(scores)), key=lambda i: scores[i])
    spec = _ARCHETYPES[best]
    return {
        "archetype_name": spec["archetype_name"],
        "interaction_signals": list(spec["interaction_signals"]),
        "danger_summary": spec["danger_summary"],
        "guardian_warning": spec["guardian_warning"],
        "risk_pressure": spec["risk_pressure"],
    }


def build_virtual_partner_profile(target: Mapping[str, Any]) -> Dict[str, Any]:
    """Shape `user_b` for bound flow from target observation fields."""
    traits = target.get("observed_traits") or []
    if isinstance(traits, str):
        traits = [traits]
    interests = [str(x).strip() for x in traits if str(x).strip()][:12]
    if not interests:
        interests = ["music", "travel", "sports"]
    inst = _bound_int(target.get("instability_level"))
    att = _bound_int(target.get("attention_demand"))
    activity = max(2, min(9, (inst + att + 3) // 2))
    return {"interests": interests, "activity": activity}


def target_object_risk_bullets(target: Mapping[str, Any]) -> List[str]:
    """Concrete '這個對象可能會…' lines from sliders + keywords (max 3)."""
    blob = _target_keyword_blob(target)
    bullets: List[str] = []
    rc = _bound_int(target.get("response_consistency"), 5)
    inst = _bound_int(target.get("instability_level"))
    att = _bound_int(target.get("attention_demand"))

    if rc <= 3 or "消失" in blob or "不回" in blob or "ghost" in blob:
        bullets.append("在需要銜接或安撫的時刻，回覆節奏可能突然變冷、變稀疏")
    if att >= 6 or "情緒" in blob or "討拍" in blob:
        bullets.append("可能經常需要大量情緒承接與即時回應，讓你的注意力被長期借走")
    if inst >= 6 or "改期" in blob or "亂" in blob:
        bullets.append("互動節奏可能不穩定，讓你較難預期下一步、神經系統容易一直待命")
    if len(bullets) < 2 and ("酸" in blob or "被動" in blob):
        bullets.append("可能用玩笑或冷處理包裝壓力，逼你花力氣讀空氣")
    if len(bullets) < 2 and ("愧疚" in blob or "情勒" in blob):
        bullets.append("可能用愧疚或情緒高低起伏，讓界線變模糊、難以離場")

    out: List[str] = []
    for b in bullets:
        if b and b not in out:
            out.append(b)
    return out[:3]


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
    optional_target: Mapping[str, Any] | None = None,
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
    if optional_target:
        raw += _bound_int(optional_target.get("attention_demand")) * 1.35
        raw += _bound_int(optional_target.get("instability_level")) * 1.05
        rc = _bound_int(optional_target.get("response_consistency"), 5)
        raw += (10 - rc) * 0.85

    interaction_risk_score = int(max(0, min(100, round(raw))))

    explanations: List[str] = [
        "這段描述的是「互動形狀」，不是在說你脆弱，也不是在說對方一定是壞人。",
        f"這類互動常見的疲勞點：{archetype.get('danger_summary', '')}",
    ]
    if optional_target:
        for b in target_object_risk_bullets(optional_target):
            if b:
                explanations.insert(1, f"觀察對象可能帶來的節奏：{b}")
                break
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
