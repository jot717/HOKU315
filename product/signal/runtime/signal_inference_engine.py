"""
Rule-based signal inference (SAFE MODE): combinations of profile, mine vector,
memory, and optional match score. No LLM, embeddings, or external APIs.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

from fox_logic import SOCIAL_MINE_KEYS, VECTOR_DIM, generate_vector
from product.memory.runtime.fox_memory_store import load_fox_memory
from product.profile.runtime.profile_store import load_profile


def _mine(vec: Sequence[float], key: str) -> float:
    idx = SOCIAL_MINE_KEYS.index(key)
    return float(vec[idx])


def collect_signal_profile_for_inference(
    insight_state: Optional[Mapping[str, Any]],
    match_score: Optional[float],
    mine_vector: Optional[Sequence[float]] = None,
) -> Dict[str, Any]:
    """
    Assemble one bundle for `infer_signal_risks` from existing stores only.

    mine_vector: optional 20-length raw slider values; if missing, uses
    profile['mine_vector'] when present and valid, else neutral 0.5s.
    """
    profile = load_profile()
    memory = load_fox_memory()
    raw: List[float]
    if mine_vector is not None and len(mine_vector) == VECTOR_DIM:
        raw = [float(x) for x in mine_vector]
    else:
        ext = profile.get("mine_vector")
        if isinstance(ext, list) and len(ext) == VECTOR_DIM:
            raw = [float(x) for x in ext]
        else:
            raw = [0.5] * VECTOR_DIM
    vec = generate_vector(raw)
    return {
        "profile": dict(profile),
        "memory": dict(memory),
        "mine_vector": vec,
        "insight_state": dict(insight_state) if insight_state else {},
        "match_score": float(match_score) if match_score is not None else None,
    }


def _bump(scores: Dict[str, float], key: str, delta: float) -> None:
    scores[key] = min(1.0, scores.get(key, 0.0) + delta)


def infer_signal_risks(signal_profile: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Pure rule engine. Returns ontology-aligned keys (see SIGNAL_RISK_ONTOLOGY.md).

    Return keys:
      risk_types, risk_scores, guardian_reasoning, high_priority_warning,
      priority (HIGH|MEDIUM|LOW), guardian_action_hint
    """
    vec = signal_profile.get("mine_vector") or [0.5] * VECTOR_DIM
    if len(vec) != VECTOR_DIM:
        vec = generate_vector([0.5] * VECTOR_DIM)
    profile = signal_profile.get("profile") or {}
    memory = signal_profile.get("memory") or {}
    insight = signal_profile.get("insight_state") or {}
    match_score = signal_profile.get("match_score")

    activity = int(profile.get("activity", 5) or 5)
    activity_n = max(0.0, min(1.0, activity / 10.0))

    recent_warnings = [str(x) for x in memory.get("recent_warnings", [])]
    recent_patterns = [str(x) for x in memory.get("recent_patterns", [])]
    memory_pressure = min(1.0, len(recent_warnings) / 5.0)
    memory_instability = min(1.0, sum("搖擺" in p for p in recent_patterns) / 3.0)

    dm = _mine(vec, "dm_pace_sensitivity")
    reply = _mine(vec, "reply_latency_anxiety")
    group = _mine(vec, "group_mention_stress")
    life_cmp = _mine(vec, "life_stage_comparison")
    humble = _mine(vec, "humblebrag_trigger")
    ambiguous = _mine(vec, "ambiguous_signals")
    excuse = _mine(vec, "excuse_skepticism")
    backhand = _mine(vec, "backhanded_praise")
    boundary = _mine(vec, "boundary_intrusion")
    cling = _mine(vec, "overcare_cling")
    tone_deaf = _mine(vec, "emotional_tone_deaf")
    silence = _mine(vec, "silence_discomfort")
    debate = _mine(vec, "values_debate_spike")
    joke = _mine(vec, "joke_boundary")

    scores: Dict[str, float] = {k: 0.0 for k in (
        "attention_drain_risk",
        "ghosting_sensitivity",
        "social_comparison_risk",
        "manipulation_sensitivity",
        "emotional_exhaustion_risk",
        "approval_dependency_risk",
        "passive_aggression_risk",
        "unsafe_circle_tolerance",
        "overexposure_risk",
        "unstable_relationship_risk",
    )}

    # Combinations (signal intelligence principle)
    fatigue_combo = 0.45 * activity_n + 0.35 * max(dm, reply) + 0.2 * group
    _bump(scores, "attention_drain_risk", fatigue_combo * 0.85)
    _bump(scores, "ghosting_sensitivity", 0.5 * reply + 0.35 * dm + 0.15 * activity_n)

    _bump(scores, "social_comparison_risk", 0.55 * life_cmp + 0.3 * humble + 0.15 * activity_n)
    _bump(scores, "approval_dependency_risk", 0.5 * humble + 0.35 * life_cmp + 0.15 * reply)

    manip_core = max(ambiguous, excuse, backhand)
    _bump(scores, "manipulation_sensitivity", 0.55 * manip_core + 0.25 * tone_deaf + 0.2 * silence)
    _bump(scores, "passive_aggression_risk", 0.45 * backhand + 0.35 * tone_deaf + 0.2 * silence)

    _bump(scores, "overexposure_risk", 0.45 * group + 0.35 * _mine(vec, "interruption_intolerance") + 0.2 * activity_n)

    _bump(scores, "unsafe_circle_tolerance", 0.45 * joke + 0.4 * debate + 0.15 * activity_n)

    _bump(scores, "unstable_relationship_risk", 0.45 * boundary + 0.4 * cling + 0.15 * ambiguous)

    _bump(scores, "emotional_exhaustion_risk", 0.55 * activity_n + 0.25 * group + 0.2 * max(dm, reply))

    _bump(scores, "attention_drain_risk", 0.15 * memory_pressure)
    _bump(scores, "manipulation_sensitivity", 0.12 * memory_instability)
    _bump(scores, "unstable_relationship_risk", 0.1 * memory_instability)

    if match_score is not None:
        ms = float(match_score)
        if ms < 45:
            _bump(scores, "emotional_exhaustion_risk", 0.12)
            _bump(scores, "attention_drain_risk", 0.1)
        if ms < 55:
            _bump(scores, "unstable_relationship_risk", 0.08)

    activity_txt = str(insight.get("activity_analysis", "") or "")
    if "tension" in activity_txt.lower() or "拉扯" in activity_txt:
        _bump(scores, "passive_aggression_risk", 0.12)
        _bump(scores, "emotional_exhaustion_risk", 0.1)

    for k in list(scores.keys()):
        scores[k] = round(max(0.0, min(1.0, scores[k])), 3)

    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    risk_types = [k for k, v in ranked if v >= 0.28][:8]
    if not risk_types:
        risk_types = [ranked[0][0]]

    top_key, top_val = ranked[0]
    second_val = ranked[1][1] if len(ranked) > 1 else 0.0

    if top_val >= 0.72 or sum(1 for _, v in ranked if v >= 0.55) >= 3:
        priority = "HIGH"
    elif top_val >= 0.48 or second_val >= 0.45:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    reasoning = _build_guardian_reasoning(ranked[:5], activity_n, reply, dm, life_cmp, manip_core)
    high_warning = _high_priority_warning(top_key, top_val, activity_n)
    action_hint = _action_hint(top_key, priority, reply, dm, group)

    return {
        "risk_types": risk_types,
        "risk_scores": scores,
        "guardian_reasoning": reasoning,
        "high_priority_warning": high_warning,
        "priority": priority,
        "guardian_action_hint": action_hint,
    }


def _build_guardian_reasoning(
    ranked_slice: List[tuple[str, float]],
    activity_n: float,
    reply: float,
    dm: float,
    life_cmp: float,
    manip_core: float,
) -> List[str]:
    lines: List[str] = []
    seen: set[str] = set()
    for key, val in ranked_slice:
        if val < 0.35:
            continue
        line: str | None = None
        if key == "attention_drain_risk" and val >= 0.4:
            line = (
                "你把注意力扣得很緊：節奏一快，就容易被訊息流帶著走，疲勞會先累積。"
            )
        elif key == "ghosting_sensitivity" and val >= 0.42:
            line = (
                "你對「已讀不回／慢回」特別敏銳，這會讓互動壓力在暗處放大。"
            )
        elif key == "manipulation_sensitivity" and val >= 0.4:
            line = (
                "模糊訊號與話中有話會讓你更費力確認安全，這是操弄壓力的常見入口。"
            )
        elif key == "social_comparison_risk" and val >= 0.4:
            line = (
                "人生進度或外在比較的話題，容易讓你把自己放到不利的位置。"
            )
        elif key == "emotional_exhaustion_risk" and val >= 0.42:
            line = (
                "你回報的壓力節奏偏高，代表身體與情緒的「續航」已經在吃老本。"
            )
        elif key == "passive_aggression_risk" and val >= 0.38:
            line = (
                "冷處理、酸話或讀不懂的沉默，會比正面衝突更耗你的力氣。"
            )
        elif key == "overexposure_risk" and val >= 0.38:
            line = (
                "群組與通知密度一高，你的神經系統會先喊累，即使事情不大。"
            )
        elif key == "unstable_relationship_risk" and val >= 0.38:
            line = (
                "邊界被踩或黏度忽高忽低時，你會更難預測下一步，消耗會上升。"
            )
        if line and line not in seen:
            seen.add(line)
            lines.append(line)
        if len(lines) >= 4:
            break
    if not lines:
        if activity_n >= 0.65:
            lines.append("壓力節奏偏高，先保護睡眠與留白，比硬扛訊息更重要。")
        else:
            lines.append("目前組合訊號相對平穩，北極狐會繼續幫你把節奏看緊。")
    return lines[:4]


def _high_priority_warning(top_key: str, top_val: float, activity_n: float) -> str:
    if top_val < 0.35:
        return "目前沒有單一壓倒性的危險型態，但仍建議維持你舒服的界線。"
    if top_key == "attention_drain_risk":
        return "注意：注意力與訊息節奏正在形成「高消耗」組合，容易在不知不覺中累垮。"
    if top_key == "ghosting_sensitivity":
        return "注意：你對回覆節奏的壓力偏高，遇到慢回或沈默時，內耗會放大。"
    if top_key == "manipulation_sensitivity":
        return "注意：話中有話與模糊承諾會讓你更警覺，這是操弄壓力的警訊。"
    if top_key == "social_comparison_risk":
        return "注意：比較與進度話題容易讓你自我縮小，這裡有社交比較風險。"
    if top_key == "emotional_exhaustion_risk":
        return "注意：主觀壓力與節奏訊號顯示，你正在接近情緒疲勞的警戒區。"
    if top_key == "passive_aggression_risk":
        return "注意：被動攻擊與曖昧訊號會讓你花更多力氣「猜」，這很耗電。"
    if top_key == "overexposure_risk":
        return "注意：曝光與打斷密度偏高，你的專注力會被切碎。"
    if top_key == "unstable_relationship_risk":
        return "注意：邊界與黏度訊號顯示關係節奏不穩，先拉開一點距離較安全。"
    if top_key == "approval_dependency_risk":
        return "注意：你對外界認可的線拉得較緊，否定式稱讚會特別刺。"
    if top_key == "unsafe_circle_tolerance":
        return "注意：尖銳玩笑或價值辯論場域，對你來說成本偏高。"
    return "注意：多個訊號疊加時，危險往往不是大事件，而是小壓力堆疊。"


def _action_hint(
    top_key: str,
    priority: str,
    reply: float,
    dm: float,
    group: float,
) -> str:
    if priority == "LOW":
        return "維持現在的距離與節奏，有需要再回觀察室更新訊號。"
    if top_key == "attention_drain_risk":
        return "先關掉最吵的通知來源，把「慢回」當正常節奏，別用刷新懲罰自己。"
    if top_key == "ghosting_sensitivity":
        return "把私訊視窗收起一陣子，告訴自己：沈默不一定是拒絕你這個人。"
    if top_key == "manipulation_sensitivity":
        return "遇到模糊承諾就停一次，要求白話與界線，別急著補齊對方的劇本。"
    if top_key == "social_comparison_risk":
        return "先離開比較場景（動態／群組），讓眼睛與心情回到自己的步調。"
    if top_key == "emotional_exhaustion_risk":
        return "今晚留一段不滑手機的空白，比再多分析都更能止血。"
    if top_key == "overexposure_risk" or group >= 0.62:
        return "群組與＠先靜音一小時，把專注還給身體，晚點再回也可以。"
    return "先減少高消耗互動，把力氣留給能讓你呼吸的人與事。"
