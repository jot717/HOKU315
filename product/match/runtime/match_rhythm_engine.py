"""
Match credibility: social energy compatibility (rhythm, cost, pressure).

Rule-based only — not dating score, personality typing, therapy, or astrology.
See docs/active/product/MATCH_ARCHETYPE_SYSTEM.md and SOCIAL_ENERGY_MODEL.md.
"""
from __future__ import annotations

import hashlib
from typing import Any, Dict, Mapping, Optional

# Match peer archetype ids (card-side interaction shape)
A_STABLE_LOW = "stable_low_pressure"
A_CALM_OBSERVER = "calm_observer"
A_LOW_MAINTENANCE = "low_maintenance"
A_HIGH_RESPONSE = "high_response_demand"
A_EMOTIONAL_EXTRACTOR = "emotional_extractor"
A_DOMINANT = "dominant_rhythm"
A_REASSURANCE = "reassurance_loop"
A_INCONSISTENT = "inconsistent_attention"
A_PERFORMER = "social_performer"
A_CONFLICT_AMP = "conflict_amplifier"
A_LOW_ENERGY_SAFE = "low_energy_safe"
A_ASYNC_SAFE = "asynchronous_safe"

_ARCHETYPE_META: Dict[str, Dict[str, str]] = {
    A_STABLE_LOW: {
        "label_zh": "穩定低壓型",
        "behavior": "回覆可預期、情緒起伏小、很少用沉默施壓。",
        "rhythm": "慢而穩，留白被允許。",
        "energy_cost": "低",
        "fatigue": "長聊才可能累，多半是時間長而非情緒重。",
    },
    A_CALM_OBSERVER: {
        "label_zh": "冷靜觀察型",
        "behavior": "傾聽多、推進少，不逼你立刻表態。",
        "rhythm": "低頻深度，不追已讀。",
        "energy_cost": "低",
        "fatigue": "若你需要高熱回饋，可能覺得「不夠投入」。",
    },
    A_LOW_MAINTENANCE: {
        "label_zh": "低維護型",
        "behavior": "小事不放大、不反覆確認關係。",
        "rhythm": "各過各的也能維持連結。",
        "energy_cost": "低",
        "fatigue": "偶爾像疏離，但很少情緒勒索。",
    },
    A_HIGH_RESPONSE: {
        "label_zh": "高回覆期待型",
        "behavior": "訊息密度高、慢回容易被追問。",
        "rhythm": "快節奏、窗口綁得緊。",
        "energy_cost": "高",
        "fatigue": "已讀與回覆速度變成隱形考試。",
    },
    A_EMOTIONAL_EXTRACTOR: {
        "label_zh": "情緒抽取型",
        "behavior": "低潮時大量傾訴，穩定後投入變少。",
        "rhythm": "你需要時他缺席、他需要時你上線。",
        "energy_cost": "高",
        "fatigue": "像一直在借電，回收卻不對稱。",
    },
    A_DOMINANT: {
        "label_zh": "主導節奏型",
        "behavior": "話題與決定常由他定調。",
        "rhythm": "單向推進，你的「先緩一緩」容易被略過。",
        "energy_cost": "中高",
        "fatigue": "為了和諧而硬跟節拍，腦力先耗盡。",
    },
    A_REASSURANCE: {
        "label_zh": "安撫迴圈型",
        "behavior": "反覆要確認、要保證，對話難收尾。",
        "rhythm": "卡在「再說一次」的循環。",
        "energy_cost": "中高",
        "fatigue": "安撫完一輪又來一輪，像沒有終點。",
    },
    A_INCONSISTENT: {
        "label_zh": "注意力搖擺型",
        "behavior": "熱絡與疏離交替，計畫常改。",
        "rhythm": "不可預測，你的神經系統常駐待命。",
        "energy_cost": "中高",
        "fatigue": "不是單次衝突，而是節奏搖擺本身耗電。",
    },
    A_PERFORMER: {
        "label_zh": "社交表演型",
        "behavior": "群組、動態、人設感強，私下卻不一定跟得上。",
        "rhythm": "公開節奏快，一對一未必同步。",
        "energy_cost": "中",
        "fatigue": "你要配合「看起來很好」的場域，休息感少。",
    },
    A_CONFLICT_AMP: {
        "label_zh": "衝突放大型",
        "behavior": "小分歧容易拉成長辯，語氣越聊越硬。",
        "rhythm": "爭論取代暫停，難真正冷卻。",
        "energy_cost": "高",
        "fatigue": "你在緊張時仍回覆，爭執變成馬拉松。",
    },
    A_LOW_ENERGY_SAFE: {
        "label_zh": "低能量安全型",
        "behavior": "不逼你熱絡、接受短回覆與慢熱。",
        "rhythm": "低刺激、可預期的接觸頻率。",
        "energy_cost": "低",
        "fatigue": "對高社交需求者可能顯得淡，但對你是保護。",
    },
    A_ASYNC_SAFE: {
        "label_zh": "非同步安全型",
        "behavior": "重視文字節奏，不懲罰晚回。",
        "rhythm": "訊息窗可拉長，不靠即時性維繫。",
        "energy_cost": "低",
        "fatigue": "較少「不回就是失敗」的壓力。",
    },
}

_USER_RISK_RHYTHM: Dict[str, str] = {
    "ghosting_sensitivity": "不穩定的回覆節奏",
    "attention_drain_risk": "高密度的訊息與注意力索取",
    "emotional_exhaustion_risk": "情緒負載過重的對話",
    "manipulation_sensitivity": "模糊承諾與話中有話的互動",
    "passive_aggression_risk": "冷處理與被動攻擊式沉默",
    "social_comparison_risk": "比較與進度話題密集的相處",
    "approval_dependency_risk": "認可釣鉤式互動",
    "overexposure_risk": "群組曝光與打斷過多的節奏",
    "unstable_relationship_risk": "邊界與黏度搖擺的關係",
    "unsafe_circle_tolerance": "價值拉鋸與辯論型對話",
}


def _top_user_risk(risk_scores: Mapping[str, float]) -> str:
    if not risk_scores:
        return "ghosting_sensitivity"
    return max(risk_scores.items(), key=lambda kv: kv[1])[0]


def _pick_peer_archetype(
    distance: float,
    conflict_dim: str,
    blurred: bool,
) -> str:
    if blurred:
        return A_CONFLICT_AMP
    seed = int(hashlib.sha256(f"{conflict_dim}|{distance:.3f}".encode()).hexdigest()[:8], 16)
    if distance <= 0.35:
        pool = [A_STABLE_LOW, A_CALM_OBSERVER, A_LOW_MAINTENANCE, A_ASYNC_SAFE, A_LOW_ENERGY_SAFE]
    elif distance < 0.7:
        pool = [A_INCONSISTENT, A_PERFORMER, A_REASSURANCE, A_CALM_OBSERVER, A_LOW_MAINTENANCE]
    else:
        pool = [A_HIGH_RESPONSE, A_EMOTIONAL_EXTRACTOR, A_DOMINANT, A_CONFLICT_AMP, A_REASSURANCE]
    return pool[seed % len(pool)]


def infer_social_rhythm(
    *,
    peer_archetype: str,
    distance: float,
    compat_bucket: str,
) -> Dict[str, str]:
    meta = _ARCHETYPE_META.get(peer_archetype, _ARCHETYPE_META[A_INCONSISTENT])
    pacing = "同步偏慢" if compat_bucket == "h" else "需刻意對齊" if compat_bucket == "m" else "易錯拍"
    return {
        "rhythm_type": meta["label_zh"],
        "rhythm_detail": meta["rhythm"],
        "interaction_pacing": pacing,
        "behavior": meta["behavior"],
    }


def infer_energy_cost(
    *,
    peer_archetype: str,
    user_risk_scores: Mapping[str, float],
    distance: float,
) -> Dict[str, str]:
    meta = _ARCHETYPE_META.get(peer_archetype, _ARCHETYPE_META[A_INCONSISTENT])
    base = meta["energy_cost"]
    top = _top_user_risk(user_risk_scores)
    bump = user_risk_scores.get(top, 0.0) if user_risk_scores else 0.0
    if distance > 0.7 or bump >= 0.55:
        safety = "偏低"
        safety_line = "與你目前的節奏敏感度疊加後，社交電量消耗可能偏快。"
    elif distance <= 0.35 and bump < 0.45:
        safety = "偏高"
        safety_line = "訊號距離近、對方節奏偏穩，你的恢復成本相對可控。"
    else:
        safety = "中等"
        safety_line = "多數場景可應付，但高壓話題仍可能拉高消耗。"
    return {
        "energy_cost_level": base,
        "energy_safety": safety,
        "energy_safety_line": safety_line,
    }


def infer_response_pressure(
    *,
    peer_archetype: str,
    user_risk_scores: Mapping[str, float],
    blurred: bool,
) -> Dict[str, str]:
    meta = _ARCHETYPE_META.get(peer_archetype, _ARCHETYPE_META[A_INCONSISTENT])
    reply_sensitive = float(user_risk_scores.get("ghosting_sensitivity", 0) or 0)
    if blurred:
        line = "在訊號未對齊前，不建議用「立刻回覆」換取安全感。"
        level = "高"
    elif peer_archetype in (A_HIGH_RESPONSE, A_REASSURANCE, A_DOMINANT):
        level = "高"
        line = "對方節奏偏快時，你可能會為了降壓而過度回覆。"
    elif peer_archetype in (A_ASYNC_SAFE, A_LOW_MAINTENANCE, A_STABLE_LOW):
        level = "低"
        line = "回覆窗可拉長，較少出現「不回就糟了」的壓力。"
    else:
        level = "中"
        line = "回覆壓力取決於當下話題，不是固定高或低。"
    if reply_sensitive >= 0.5 and level != "低":
        line += " 你對慢回較敏感，這會放大上述壓力。"
    return {
        "reply_pressure_level": level,
        "reply_pressure_line": line,
        "communication_pressure": f"溝通壓力：{level}（{meta['label_zh']}）",
    }


def infer_interaction_stability(
    *,
    distance: float,
    compat_bucket: str,
    blurred: bool,
) -> Dict[str, str]:
    if blurred:
        return {
            "stability": "未知",
            "stability_line": "系統先遮蔽高落差組合，避免你在節奏不明時過度投入。",
        }
    if compat_bucket == "h":
        return {
            "stability": "較穩",
            "stability_line": "互動形狀可預期，較少突然的情緒加速或冷卻。",
        }
    if compat_bucket == "l":
        return {
            "stability": "偏搖擺",
            "stability_line": "節奏錯拍時，小摩擦也可能被拉長成消耗戰。",
        }
    return {
        "stability": "中等",
        "stability_line": "穩定度取決於話題；需要時把對話放慢。",
    }


def generate_insight_weakness_link(
    *,
    inference: Optional[Mapping[str, Any]] = None,
    relationship_simulation: Optional[Mapping[str, Any]] = None,
) -> str:
    """Connect user rhythm weakness ↔ interaction type that triggers it."""
    inf = inference or {}
    scores = inf.get("risk_scores") if isinstance(inf.get("risk_scores"), dict) else {}
    top = _top_user_risk(scores)
    rhythm_phrase = _USER_RISK_RHYTHM.get(top, "高消耗互動節奏")
    val = float(scores.get(top, 0) or 0)
    if val < 0.35:
        return (
            "你目前的問卷訊號裡，沒有單一壓倒性的節奏弱點；"
            "仍建議在「回覆變快、話題變重」時先放慢一步。"
        )
    sim = relationship_simulation or {}
    matches = [str(x) for x in sim.get("risk_matches", [])[:1]]
    tail = f"（與觀察對象重疊：{matches[0]}）" if matches else ""
    return (
        f"你容易在「{rhythm_phrase}」裡待太久——"
        f"多半是節奏與恢復時間沒對上，而不是你「撐不住」。{tail}"
    )


def generate_match_credibility_bundle(
    *,
    distance: float,
    compat_bucket: str,
    conflict_dim_label: str = "",
    blurred: bool = False,
    user_inference: Optional[Mapping[str, Any]] = None,
    profile: Optional[Mapping[str, Any]] = None,
) -> Dict[str, str]:
    """
    Card-ready copy: rhythm, reply pressure, pacing, energy safety, exhaustion, scenario.
    """
    _ = profile
    inf = user_inference or {}
    scores = inf.get("risk_scores") if isinstance(inf.get("risk_scores"), dict) else {}
    peer = _pick_peer_archetype(distance, conflict_dim_label, blurred)
    meta = _ARCHETYPE_META[peer]

    rhythm = infer_social_rhythm(
        peer_archetype=peer, distance=distance, compat_bucket=compat_bucket
    )
    energy = infer_energy_cost(
        peer_archetype=peer, user_risk_scores=scores, distance=distance
    )
    pressure = infer_response_pressure(
        peer_archetype=peer, user_risk_scores=scores, blurred=blurred
    )
    stability = infer_interaction_stability(
        distance=distance, compat_bucket=compat_bucket, blurred=blurred
    )

    if blurred:
        scenario = (
            "例如：對方連續追問時，你先約定「晚點回」再開聊——"
            "在節奏不明前，不要用即時回覆換安心。"
        )
    elif compat_bucket == "h":
        scenario = (
            "例如：你晚幾小時回，對方不追問、話題也不變味——"
            "這種非同步通常代表社交電量較省。"
        )
    elif compat_bucket == "m":
        scenario = (
            "例如：群組裡對方@你，你可以先已讀慢回，"
            "而不必立刻進入高能量語氣。"
        )
    else:
        scenario = (
            "例如：話題轉重時，你若開始解釋很多、對方只回短句——"
            "這往往是節奏錯拍，不是你不夠努力。"
        )

    emotional_pacing = (
        f"情緒步調：{meta['label_zh']} — "
        f"{'起伏偏大' if peer in (A_INCONSISTENT, A_EMOTIONAL_EXTRACTOR, A_CONFLICT_AMP) else '相對平緩'}"
    )

    return {
        "peer_archetype": peer,
        "rhythm_type": rhythm["rhythm_type"],
        "interaction_rhythm_line": f"互動節奏：{rhythm['rhythm_type']} — {rhythm['rhythm_detail']}",
        "reply_pressure_line": f"回覆壓力：{pressure['reply_pressure_line']}",
        "emotional_pacing_line": emotional_pacing,
        "energy_safety_line": f"社交電量安全度：{energy['energy_safety']} — {energy['energy_safety_line']}",
        "exhaustion_point_line": f"可能耗盡點：{meta['fatigue']}",
        "communication_pressure": pressure["communication_pressure"],
        "interaction_pacing": rhythm["interaction_pacing"],
        "fatigue_risk": meta["energy_cost"],
        "stability_line": stability["stability_line"],
        "scenario_line": scenario,
        "lighter_line": (
            f"相處較省力之處：{meta['behavior'][:40]}…"
            if compat_bucket != "l"
            else f"此組合節奏偏耗電：{meta['behavior'][:36]}…"
        ),
        "pressure_reduced_line": energy["energy_safety_line"],
    }
