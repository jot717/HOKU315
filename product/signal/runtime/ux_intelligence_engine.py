"""
Rule-based UX intelligence: social pressure interpretation (no LLM, no therapy).

Maps profile, mine vector inference, target, and relationship simulation into
short causal copy for insight and match surfaces.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

# Ontology pattern ids (see INTERACTION_PRESSURE_ONTOLOGY.md)
P_EMOTIONAL_LABOR = "emotional_labor_trap"
P_REASSURANCE_LOOP = "endless_reassurance_loop"
P_RESPONSE_PRESSURE = "response_pressure"
P_DOMINANCE = "dominance_interaction"
P_PASSIVE_GUILT = "passive_guilt_pressure"
P_VALIDATION = "validation_extraction"
P_COMPARISON = "comparison_exhaustion"
P_PERFORMANCE = "social_performance_fatigue"
P_UNSTABLE_RHYTHM = "unstable_rhythm_stress"
P_VALUE_DEBATE = "value_debate_burnout"
P_INTIMACY_RUSH = "intimacy_acceleration"
P_INCONSISTENCY = "inconsistency_anxiety"
P_UNPREDICTABILITY = "emotional_unpredictability"
P_ATTENTION_ASYM = "attention_asymmetry"
P_CONFLICT_AVOID = "conflict_avoidance_exhaustion"

_RISK_TO_PRESSURE: Dict[str, str] = {
    "attention_drain_risk": P_ATTENTION_ASYM,
    "ghosting_sensitivity": P_RESPONSE_PRESSURE,
    "social_comparison_risk": P_COMPARISON,
    "manipulation_sensitivity": P_PASSIVE_GUILT,
    "emotional_exhaustion_risk": P_EMOTIONAL_LABOR,
    "approval_dependency_risk": P_VALIDATION,
    "passive_aggression_risk": P_PASSIVE_GUILT,
    "unsafe_circle_tolerance": P_VALUE_DEBATE,
    "overexposure_risk": P_PERFORMANCE,
    "unstable_relationship_risk": P_UNSTABLE_RHYTHM,
}

_SIGNAL_TO_PRESSURE: Dict[str, str] = {
    "delayed reassurance": P_REASSURANCE_LOOP,
    "emotional ambiguity": P_INCONSISTENCY,
    "emotional unpredictability": P_UNPREDICTABILITY,
    "attention extraction": P_ATTENTION_ASYM,
    "pressure escalation": P_DOMINANCE,
    "validation farming": P_VALIDATION,
    "passive hostility": P_PASSIVE_GUILT,
    "guilt-driven interaction": P_PASSIVE_GUILT,
    "social comparison pressure": P_COMPARISON,
    "unstable affection": P_UNSTABLE_RHYTHM,
}

_PRESSURE_COPY: Dict[str, Dict[str, str]] = {
    P_EMOTIONAL_LABOR: {
        "drain": "你常在對方低潮時自動補位，久了會像一直在付情緒勞動，而不是單純聊天。",
        "rhythm": "節奏偏向「對方需要你就回」，你的恢復時間被擠到邊角。",
        "avoid": "長期只出不進的情緒承接，會把你的社交電量磨平。",
        "fit": "相處時不必當情緒急救箱，互動會比較輕。",
    },
    P_REASSURANCE_LOOP: {
        "drain": "安撫像沒有終點：你安撫完一輪，對方又需要下一輪保證。",
        "rhythm": "對話卡在「再確認一次」的迴圈，很難真正結束。",
        "avoid": "反覆求保證的互動，會讓你覺得怎麼回都不夠。",
        "fit": "對方情緒能自己落地，你就不必一直當回音壁。",
    },
    P_RESPONSE_PRESSURE: {
        "drain": "已讀與回覆速度變成隱形考試，你會為了不讓氣氛冷掉而硬撐。",
        "rhythm": "節奏被訊息窗綁住，很難自然留白。",
        "avoid": "把慢回當成失敗的關係，會讓你持續緊繃。",
        "fit": "允許隔幾小時再回，互動壓力會明顯下降。",
    },
    P_DOMINANCE: {
        "drain": "話題與決定常被對方帶走，你要花力氣才能把自己的步調插回去。",
        "rhythm": "節奏像單向推進，你的邊界容易被略過。",
        "avoid": "總要配合對方節拍的相處，會讓你覺得沒有退出鍵。",
        "fit": "意見能輪流主導，你比較不用一直防守。",
    },
    P_PASSIVE_GUILT: {
        "drain": "酸話、冷處理或「都是為你好」會讓你反覆檢討自己。",
        "rhythm": "衝突不正面爆開，卻用內疚拖住你，比吵架更耗神。",
        "avoid": "用愧疚換配合的互動，會讓你不敢說不。",
        "fit": "有分歧能直接講，你比較不用猜空氣。",
    },
    P_VALIDATION: {
        "drain": "讚美像釣鉤：你越想證明自己，對方越不給清楚回應。",
        "rhythm": "節奏變成「你表現 → 對方點頭 → 你再表現」。",
        "avoid": "靠外在肯定才能安心的相處，會讓你越做越累。",
        "fit": "肯定具體、不吊胃口，你比較不用一直證明。",
    },
    P_COMPARISON: {
        "drain": "進度、成就或生活樣板一出現，你就容易把自己放到較差的位置。",
        "rhythm": "對話常滑向比較場，你的注意力被拉去對標。",
        "avoid": "充滿「別人都…」的話題，會讓你社交後特別空。",
        "fit": "少比較、多描述自己的日子，你比較能放鬆。",
    },
    P_PERFORMANCE: {
        "drain": "群組或動態像舞台，你要維持人設，休息感很少。",
        "rhythm": "節奏快、曝光高，你的專注被切成碎片。",
        "avoid": "一直要「看起來還好」的場合，會讓你假裝不累。",
        "fit": "可以素顏出現、不必表演，恢復會快很多。",
    },
    P_UNSTABLE_RHYTHM: {
        "drain": "熱絡與疏離交替，你的神經系統像一直在待命。",
        "rhythm": "節奏忽快忽慢，你難以預測下一步要投入多少。",
        "avoid": "計畫常改、情緒起伏大的互動，會堆出隱性疲勞。",
        "fit": "節奏可預期，你比較不用隨時調整防備。",
    },
    P_VALUE_DEBATE: {
        "drain": "價值觀拉鋸會把你捲進辯論，而不是單純交流。",
        "rhythm": "對話容易變成誰對誰錯，而不是一起休息。",
        "avoid": "動不動就上價值戰場的相處，會讓你社交後腦袋發燙。",
        "fit": "分歧能暫停、不必當場定輸贏，你比較省電。",
    },
    P_INTIMACY_RUSH: {
        "drain": "親密推太快，你還沒確認安全就得跟著加深。",
        "rhythm": "節奏像被快轉，你的界線來不及長出來。",
        "avoid": "前期過度承諾、後期變要求的劇本，會讓你懷疑自己。",
        "fit": "信任慢慢累積，你比較不用急著表態。",
    },
    P_INCONSISTENCY: {
        "drain": "訊號前後不一，你會花很多力氣對齊「他到底什麼意思」。",
        "rhythm": "節奏像解謎，而不是自然來回。",
        "avoid": "態度搖擺的互動，會讓你比正面衝突更累。",
        "fit": "態度一致、說到做到，你比較不用腦內補劇。",
    },
    P_UNPREDICTABILITY: {
        "drain": "情緒與回應難以預測，你會一直預留心理緩衝。",
        "rhythm": "節奏不穩，你的休息永遠是暫時的。",
        "avoid": "能量忽高忽低的相處，會讓疲勞在背景累積。",
        "fit": "情緒起伏可預期，你比較敢放鬆靠近。",
    },
    P_ATTENTION_ASYM: {
        "drain": "你的注意力付出多、回收少，像一直在借電給對方。",
        "rhythm": "節奏不對等：你回得快，對方回得慢或只在自己需要時出現。",
        "avoid": "只在你有空時才被找、你忙時就消失的互動。",
        "fit": "投入與回應大致對稱，你比較不會覺得被掏空。",
    },
    P_CONFLICT_AVOID: {
        "drain": "你傾向在緊張時仍維持回覆，爭執就慢慢變成耗竭而不是結束。",
        "rhythm": "節奏卡在「不能冷場」，很難真正暫停。",
        "avoid": "一直用配合換和平，問題沒解決、疲勞先堆高。",
        "fit": "可以約定先冷卻再談，你比較不用硬撐語氣。",
    },
}


def _ranked_pressures(
    risk_scores: Mapping[str, float],
    risk_types: Sequence[str],
    interaction_signals: Sequence[str],
) -> List[str]:
    scores: Dict[str, float] = {}
    for rk, pid in _RISK_TO_PRESSURE.items():
        v = float(risk_scores.get(rk, 0) or 0)
        if v > 0:
            scores[pid] = max(scores.get(pid, 0.0), v)
    for sig in interaction_signals:
        pid = _SIGNAL_TO_PRESSURE.get(str(sig).strip().lower())
        if pid:
            scores[pid] = max(scores.get(pid, 0.0), 0.55)
    for rt in risk_types:
        pid = _RISK_TO_PRESSURE.get(str(rt).strip())
        if pid:
            scores[pid] = max(scores.get(pid, 0.0), 0.5)
    if not scores:
        return [P_RESPONSE_PRESSURE]
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    return [k for k, _ in ranked[:4]]


def generate_pressure_explanations(
    *,
    profile: Optional[Mapping[str, Any]] = None,
    inference: Optional[Mapping[str, Any]] = None,
    relationship_simulation: Optional[Mapping[str, Any]] = None,
    interaction_signals: Optional[Sequence[str]] = None,
) -> List[str]:
    """Short bullets: what pressure patterns are active."""
    inf = inference or {}
    sim = relationship_simulation or {}
    scores = inf.get("risk_scores") if isinstance(inf.get("risk_scores"), dict) else {}
    types = inf.get("risk_types") if isinstance(inf.get("risk_types"), list) else []
    sigs = list(interaction_signals or [])
    for m in sim.get("risk_matches", [])[:3]:
        sigs.append(str(m))
    patterns = _ranked_pressures(scores, types, sigs)
    lines: List[str] = []
    for pid in patterns[:3]:
        line = _PRESSURE_COPY.get(pid, {}).get("drain", "")
        if line and line not in lines:
            lines.append(line)
    return lines


def generate_avoidance_reasoning(
    *,
    profile: Optional[Mapping[str, Any]] = None,
    inference: Optional[Mapping[str, Any]] = None,
    relationship_simulation: Optional[Mapping[str, Any]] = None,
    archetype: Optional[Mapping[str, Any]] = None,
) -> str:
    inf = inference or {}
    arch = archetype or {}
    scores = inf.get("risk_scores") if isinstance(inf.get("risk_scores"), dict) else {}
    sigs = list(arch.get("interaction_signals") or [])
    patterns = _ranked_pressures(
        scores,
        inf.get("risk_types") if isinstance(inf.get("risk_types"), list) else [],
        sigs,
    )
    pid = patterns[0]
    base = _PRESSURE_COPY.get(pid, {}).get("avoid", "")
    summary = str(arch.get("danger_summary", "")).strip()
    if summary and len(base) < 80:
        return f"{base} 這段互動裡，{summary}"
    return base or "先減少會讓你反覆猜測、或只出不進的相處節奏。"


def generate_match_fit_reasoning(
    *,
    distance: float,
    compat_bucket: str,
    conflict_dim_label: str = "",
    blurred: bool = False,
    inference: Optional[Mapping[str, Any]] = None,
    profile: Optional[Mapping[str, Any]] = None,
) -> Dict[str, str]:
    """Per-card social causality for match wall (precomputed in enrich)."""
    inf = inference or {}
    scores = inf.get("risk_scores") if isinstance(inf.get("risk_scores"), dict) else {}
    top_risk = max(scores.items(), key=lambda kv: kv[1])[0] if scores else "attention_drain_risk"
    pid = _RISK_TO_PRESSURE.get(top_risk, P_RESPONSE_PRESSURE)
    copy = _PRESSURE_COPY.get(pid, _PRESSURE_COPY[P_RESPONSE_PRESSURE])

    if blurred:
        return {
            "lighter_line": "此對象訊號落差較大，系統先模糊處理，避免你誤入高壓節奏。",
            "pressure_reduced_line": "暫時看不到細節，但已先擋掉最可能放大你回覆壓力的組合。",
            "rhythm_line": "解鎖前請先假設：節奏可能不對等，不要為了確認而硬撐回覆。",
            "fatigue_avoided_line": "避免在訊號不明時投入情緒勞動。",
            "scenario_line": "若解鎖後發現對話常讓你「不回就內疚」，建議把回覆窗拉大。",
        }

    if compat_bucket == "h":
        lighter = (
            "互動不必一直解釋自己，對話比較像並肩而不是單向審核。"
        )
        reduced = copy.get("fit", "相處時你比較不用當情緒急救箱。")
        rhythm = (
            "回覆節奏接近：你可以慢一點回，而不必擔心關係立刻變味。"
            if distance <= 0.35
            else "多數時候你們的節奏能對上，不必靠硬撐維持熱度。"
        )
        fatigue = f"較不容易觸發你的「{copy.get('avoid', '高消耗互動')[:24]}…」型疲勞。"
        scenario = (
            "例如：約好改天再聊，雙方都不會用已讀來施壓——這種小事會讓你比較省電。"
        )
    elif compat_bucket == "m":
        lighter = "有些場景輕鬆，但仍有幾個維度需要你留意步調。"
        reduced = f"衝突點在「{conflict_dim_label}」附近時，把對話放慢比加碼解釋有效。"
        rhythm = copy.get("rhythm", "節奏時快時慢，適合先觀察再加深投入。")
        fatigue = copy.get("avoid", "避免在曖昧或比較話題上硬撐。")
        scenario = (
            "例如：群組裡對方@你時，你可以晚一點回，而不必立刻進入表演模式。"
        )
    else:
        lighter = "靠近時容易覺得「要配合對方」，而不是自然聊天。"
        reduced = "系統仍列出是讓你看見落差，不代表你必須硬磨合。"
        rhythm = copy.get("rhythm", "節奏落差大，回覆壓力可能先於好感出現。")
        fatigue = copy.get("avoid", "這類組合常讓你在不自覺中多付一輪情緒勞動。")
        scenario = (
            "例如：對方連續追問時，你若覺得喘，先暫停比解釋更重要——這是節奏問題，不是你不夠好。"
        )

    return {
        "lighter_line": lighter,
        "pressure_reduced_line": reduced,
        "rhythm_line": rhythm,
        "fatigue_avoided_line": fatigue,
        "scenario_line": scenario,
    }


def generate_interaction_reasoning(
    *,
    profile: Optional[Mapping[str, Any]] = None,
    quiz_vector: Optional[Sequence[float]] = None,
    target_profile: Optional[Mapping[str, Any]] = None,
    inference: Optional[Mapping[str, Any]] = None,
    relationship_simulation: Optional[Mapping[str, Any]] = None,
    archetype: Optional[Mapping[str, Any]] = None,
    match_score: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Full insight bundle: drain line, rhythm conflict, fit, avoid, fox observer (one block).
    """
    inf = inference or {}
    arch = archetype or {}
    tgt = target_profile or {}
    sim = relationship_simulation or {}
    scores = inf.get("risk_scores") if isinstance(inf.get("risk_scores"), dict) else {}
    sigs = list(arch.get("interaction_signals") or [])
    patterns = _ranked_pressures(
        scores,
        inf.get("risk_types") if isinstance(inf.get("risk_types"), list) else [],
        sigs,
    )
    primary = patterns[0]
    copy = _PRESSURE_COPY.get(primary, _PRESSURE_COPY[P_RESPONSE_PRESSURE])

    target_name = str(tgt.get("target_name", "")).strip()
    arch_name = str(arch.get("archetype_name", "")).strip()

    pressures = generate_pressure_explanations(
        profile=profile,
        inference=inf,
        relationship_simulation=sim,
        interaction_signals=sigs,
    )

    why_drains = pressures[0] if pressures else copy["drain"]
    if target_name:
        why_drains = (
            f"面對「{target_name}」時，{why_drains.lstrip('你')}"
            if why_drains.startswith("你")
            else f"面對「{target_name}」：{why_drains}"
        )

    rhythm = copy["rhythm"]
    if arch_name:
        rhythm = f"{arch_name} 的節奏下，{rhythm}"

    fit = copy["fit"]
    if match_score is not None and match_score >= 70:
        fit = f"訊號距離較近時，{fit}"
    elif match_score is not None and match_score < 50:
        fit = "目前距離偏遠，先觀察節奏比急著拉近更重要。"

    avoid = generate_avoidance_reasoning(
        profile=profile,
        inference=inf,
        relationship_simulation=sim,
        archetype=arch,
    )

    fox = _fox_observer_line(
        primary=primary,
        target_name=target_name,
        match_score=match_score,
        priority=str(inf.get("priority", "LOW")),
    )

    return {
        "why_drains": why_drains,
        "rhythm_conflict": rhythm,
        "pressure_bullets": pressures,
        "fit_reasoning": fit,
        "avoid_reasoning": avoid,
        "fox_observer": fox,
        "primary_pressure_id": primary,
    }


def _fox_observer_line(
    *,
    primary: str,
    target_name: str,
    match_score: Optional[float],
    priority: str,
) -> str:
    """Single quiet observer note — not therapy, not mascot."""
    if priority == "HIGH":
        lead = "我注意到：這段互動裡，壓力多半來自節奏，而不是你「做錯了什麼」。"
    elif match_score is not None and match_score >= 75:
        lead = "我注意到：你們的節奏有餘裕，不必為了維持熱度而多付一輪力氣。"
    else:
        lead = "我注意到：你在意回覆與氛圍，所以小落差也會被放大——這是訊號敏感，不是性格缺陷。"

    hint = _PRESSURE_COPY.get(primary, {}).get("drain", "")
    if target_name:
        tail = f" 若「{target_name}」常在 {_pressure_label_zh(primary)} 附近消耗你，先把回覆窗拉大會比解釋有效。"
    else:
        tail = f" 當 {_pressure_label_zh(primary)} 出現時，先保護留白，比立刻把對話救回來更重要。"
    return f"{lead}{tail}"


def _pressure_label_zh(pid: str) -> str:
    labels = {
        P_EMOTIONAL_LABOR: "情緒勞動",
        P_REASSURANCE_LOOP: "安撫迴圈",
        P_RESPONSE_PRESSURE: "回覆壓力",
        P_DOMINANCE: "單向主導",
        P_PASSIVE_GUILT: "內疚施壓",
        P_VALIDATION: "認可索取",
        P_COMPARISON: "比較消耗",
        P_PERFORMANCE: "社交表演",
        P_UNSTABLE_RHYTHM: "節奏搖擺",
        P_VALUE_DEBATE: "價值拉鋸",
        P_INTIMACY_RUSH: "親密快轉",
        P_INCONSISTENCY: "訊號不一致",
        P_UNPREDICTABILITY: "情緒難測",
        P_ATTENTION_ASYM: "注意力不對等",
        P_CONFLICT_AVOID: "迴避式耗竭",
    }
    return labels.get(pid, "互動壓力")
