from __future__ import annotations

from typing import Any, Dict, List

import reflex as rx

from product.app_binding.runtime.flow_binding import execute_bound_flow
from product.app_binding.runtime.persistence import load_session
from product.guard.runtime.signal_guard_engine import evaluate_signal_risk
from product.insight.experience.fox_narration import build_fox_message
from product.insight.experience.insight_formatter import format_emotional_insight
from product.insight.experience.reveal_engine import build_reveal_state
from product.memory.runtime.fox_memory_engine import (
    apply_inference_memory_tags,
    record_relationship_simulation_memory,
    record_target_pattern_memory,
    remember_insight,
)
from product.memory.runtime.fox_memory_store import get_memory_display
from product.profile.runtime.profile_store import load_profile
from product.session.runtime.session_history import append_history, load_history
from product.signal.runtime.relationship_simulation_engine import (
    archetype_for_target_profile,
    build_virtual_partner_profile,
    generate_relationship_archetype,
    simulate_relationship_risk,
    target_object_risk_bullets,
)
from product.signal.runtime.signal_inference_engine import (
    collect_signal_profile_for_inference,
    infer_signal_risks,
)
from product.signal.runtime.ux_intelligence_engine import generate_interaction_reasoning
from product.target.runtime.target_profile_store import load_target_profile


def _str_list(values: Any, *, limit: int) -> List[str]:
    """Plain strings for Reflex state / hydration (no mixed nested types)."""
    if values is None:
        return []
    if isinstance(values, str):
        s = values.strip()
        return [s] if s else []
    if not isinstance(values, (list, tuple)):
        return []
    out: List[str] = []
    for x in values:
        s = str(x).strip()
        if s:
            out.append(s)
        if len(out) >= limit:
            break
    return out


def _match_score_from_flow(flow: Dict[str, Any]) -> float:
    if not isinstance(flow, dict):
        return 0.0
    m = flow.get("match")
    if not isinstance(m, dict):
        m = {}
    try:
        return float(m.get("score", 0))
    except (TypeError, ValueError):
        return 0.0


def _fallback_guardian_why_lines(flags: List[str], risk_level: str) -> List[str]:
    """Rule-based bullets when inference reasoning is empty."""
    lines: List[str] = []
    flagset = set(flags)
    if "高壓節奏" in flagset or "消耗傾向" in flagset:
        lines.append("最近重複出現高壓互動")
    if "訊號不穩定" in flagset or "節奏失衡" in flagset:
        lines.append("壓力節奏沒有恢復空間")
    if "過度比較" in flagset or "低共鳴" in flagset:
        lines.append("某些訊號正在反覆消耗你")
    if not lines and risk_level != "low":
        lines.append("訊號節奏仍需要你多留一步空間")
    if not lines:
        lines.append("目前守護視野裡沒有明顯危險")
    return lines[:3]


class AppState(rx.State):
    flow_result: Dict[str, Any] = {}
    insight_state: Dict[str, Any] = {}

    demo_match_loading: bool = False

    session_history: List[Dict[str, Any]] = []

    compatibility_title: str = ""
    energy_summary: str = ""
    final_insight: str = ""

    reveal_level: str = ""
    reveal_delay: float = 0.0
    show_final_card: bool = False

    fox_message: str = ""

    fox_memory_note: str = ""
    recurring_pattern: str = ""
    signal_risk_level: str = "low"
    signal_risk_flags: List[str] = []
    guardian_warning: str = ""
    guardian_action: str = ""

    display_risk_level: str = "low"
    signal_inference_types: List[str] = []
    inference_risk_scores: Dict[str, float] = {}
    inference_priority_label: str = "LOW"
    inference_high_warning: str = ""
    inference_guardian_reasoning: List[str] = []
    guardian_why_lines: List[str] = []

    relationship_archetype_name: str = ""
    relationship_archetype_pressure: str = ""
    relationship_archetype_danger_summary: str = ""
    relationship_archetype_guardian_hint: str = ""
    relationship_interaction_risk_score: int = 0
    relationship_explanation_lines: List[str] = []
    guardian_simulation_advice: str = ""
    guardian_interaction_framing: str = "你不需要自己承受所有壓力。"

    insight_target_name: str = ""
    insight_target_relationship: str = ""

    ux_why_drains_line: str = ""
    ux_rhythm_conflict_line: str = ""
    ux_pressure_bullets: List[str] = []
    ux_fit_reasoning: str = ""
    ux_avoid_reasoning: str = ""
    ux_fox_observer_note: str = ""

    @rx.var(cache=True)
    def has_insight(self) -> bool:
        return isinstance(self.insight_state, dict) and bool(self.insight_state)

    @rx.var(cache=True)
    def has_relationship_explanation_lines(self) -> bool:
        return bool(self.relationship_explanation_lines)

    @rx.var(cache=True)
    def has_signal_inference_types(self) -> bool:
        return bool(self.signal_inference_types)

    @rx.var(cache=True)
    def insight_communication_rhythm_line(self) -> str:
        rhythm = (self.ux_rhythm_conflict_line or "").strip()
        if rhythm:
            return rhythm
        name = (self.relationship_archetype_name or "").strip()
        pressure = (self.relationship_archetype_pressure or "").strip()
        if name and pressure:
            return f"{name} · 壓力標記：{pressure}"
        if name:
            return name
        if pressure:
            return f"壓力標記：{pressure}"
        return "（尚未成形）"

    @rx.var(cache=True)
    def ux_pressure_bullets_formatted(self) -> str:
        return self._bullet_block(self.ux_pressure_bullets, limit=3)

    @staticmethod
    def _bullet_block(items: List[str], *, limit: int) -> str:
        out: List[str] = []
        for x in (items or [])[:limit]:
            s = str(x).strip()
            if s:
                out.append(f"・ {s}")
        return "\n".join(out)

    @rx.var(cache=True)
    def guardian_why_bullets_formatted(self) -> str:
        return self._bullet_block(self.guardian_why_lines, limit=8)

    @rx.var(cache=True)
    def relationship_explanation_bullets_formatted(self) -> str:
        return self._bullet_block(self.relationship_explanation_lines, limit=8)

    @rx.var(cache=True)
    def signal_inference_bullets_formatted(self) -> str:
        return self._bullet_block(self.signal_inference_types, limit=16)

    @rx.var(cache=True)
    def match_score_safe_int(self) -> int:
        """0–100 int for rx.progress (requires int, not float)."""
        fr = self.flow_result if isinstance(self.flow_result, dict) else {}
        m = fr.get("match")
        if not isinstance(m, dict):
            m = {}
        try:
            s = float(m.get("score", 0))
        except (TypeError, ValueError):
            s = 0.0
        return max(0, min(100, int(round(s))))

    @rx.var(cache=True)
    def match_score_heading(self) -> str:
        fr = self.flow_result if isinstance(self.flow_result, dict) else {}
        m = fr.get("match")
        if not isinstance(m, dict):
            m = {}
        try:
            raw = float(m.get("score", 0))
        except (TypeError, ValueError):
            raw = 0.0
        safe = max(0, min(100, int(round(raw))))
        return f"{safe}%"

    def _refresh_fox_memory_from_store(self) -> None:
        display = get_memory_display()
        self.fox_memory_note = str(display.get("guardian_memory_note", ""))
        self.recurring_pattern = str(display.get("recurring_pattern", ""))

    def _apply_emotional_insight(self) -> None:
        if not isinstance(self.insight_state, dict) or not self.insight_state:
            self.compatibility_title = ""
            self.energy_summary = ""
            self.final_insight = ""
            self.reveal_level = ""
            self.reveal_delay = 0.0
            self.show_final_card = False
            self.fox_message = ""
            self.signal_risk_level = "low"
            self.signal_risk_flags = []
            self.guardian_warning = ""
            self.guardian_action = ""
            self.display_risk_level = "low"
            self.signal_inference_types = []
            self.inference_risk_scores = {}
            self.inference_priority_label = "LOW"
            self.inference_high_warning = ""
            self.inference_guardian_reasoning = []
            self.guardian_why_lines = []
            self.relationship_archetype_name = ""
            self.relationship_archetype_pressure = ""
            self.relationship_archetype_danger_summary = ""
            self.relationship_archetype_guardian_hint = ""
            self.relationship_interaction_risk_score = 0
            self.relationship_explanation_lines = []
            self.guardian_simulation_advice = ""
            self.guardian_interaction_framing = "你不需要自己承受所有壓力。"
            self.insight_target_name = ""
            self.insight_target_relationship = ""
            self.ux_why_drains_line = ""
            self.ux_rhythm_conflict_line = ""
            self.ux_pressure_bullets = []
            self.ux_fit_reasoning = ""
            self.ux_avoid_reasoning = ""
            self.ux_fox_observer_note = ""
            self._refresh_fox_memory_from_store()
            return

        score = _match_score_from_flow(self.flow_result)
        emotional = format_emotional_insight(self.insight_state, score)
        self.compatibility_title = str(emotional.get("compatibility_title", "") or "")
        self.energy_summary = str(emotional.get("energy_summary", "") or "")
        self.final_insight = str(emotional.get("final_insight", "") or "")

        reveal = build_reveal_state(self.insight_state, score)
        self.reveal_level = str(reveal["level"])
        self.reveal_delay = float(reveal["reveal_delay"])
        self.show_final_card = bool(reveal["show_final_card"])

        self.fox_message = build_fox_message(
            self.insight_state,
            score,
        )
        guard = evaluate_signal_risk(self.insight_state, score)
        self.signal_risk_level = str(guard.get("risk_level", "low"))
        self.signal_risk_flags = [
            str(x) for x in guard.get("risk_flags", []) if str(x).strip()
        ]
        self.guardian_warning = str(guard.get("guardian_warning", ""))
        guard_action = str(guard.get("guardian_action", ""))
        self.guardian_action = guard_action

        bundle = collect_signal_profile_for_inference(self.insight_state, score, None)
        inf = infer_signal_risks(bundle)
        self.signal_inference_types = _str_list(inf.get("risk_types"), limit=32)
        raw_rs = inf.get("risk_scores")
        scored: Dict[str, float] = {}
        if isinstance(raw_rs, dict):
            for k, v in raw_rs.items():
                try:
                    scored[str(k)] = float(v)
                except (TypeError, ValueError):
                    continue
        self.inference_risk_scores = scored
        self.inference_priority_label = str(inf.get("priority", "LOW")).upper()
        self.inference_high_warning = str(inf.get("high_priority_warning", ""))
        self.inference_guardian_reasoning = _str_list(inf.get("guardian_reasoning"), limit=4)
        hint = str(inf.get("guardian_action_hint", "")).strip()

        inf_rank = {"HIGH": 2, "MEDIUM": 1, "LOW": 0}.get(self.inference_priority_label, 0)
        g_rank = {"high": 2, "medium": 1, "low": 0}.get(str(self.signal_risk_level).lower(), 0)
        merged = max(inf_rank, g_rank)
        self.display_risk_level = "high" if merged == 2 else "medium" if merged == 1 else "low"

        if self.inference_guardian_reasoning:
            self.guardian_why_lines = self.inference_guardian_reasoning[:3]
        else:
            self.guardian_why_lines = _fallback_guardian_why_lines(
                self.signal_risk_flags,
                self.signal_risk_level,
            )

        if inf_rank > g_rank or (inf_rank >= 1 and hint):
            self.guardian_action = hint or guard_action

        tgt = load_target_profile()
        self.insight_target_name = str(tgt.get("target_name", "")).strip()
        self.insight_target_relationship = str(tgt.get("relationship_type", "")).strip()
        has_target = bool(self.insight_target_name)

        arch = (
            archetype_for_target_profile(tgt)
            if has_target
            else generate_relationship_archetype()
        )
        self.relationship_archetype_name = str(arch.get("archetype_name", ""))
        self.relationship_archetype_pressure = str(arch.get("risk_pressure", "LOW"))
        self.relationship_archetype_danger_summary = str(arch.get("danger_summary", ""))
        self.relationship_archetype_guardian_hint = str(arch.get("guardian_warning", ""))
        user_sig = {
            "risk_scores": self.inference_risk_scores,
            "risk_types": self.signal_inference_types,
            "profile": bundle.get("profile", {}),
        }
        sim = simulate_relationship_risk(
            user_sig,
            arch,
            tgt if has_target else None,
        )
        self.relationship_interaction_risk_score = int(sim.get("interaction_risk_score", 0))
        self.relationship_explanation_lines = _str_list(sim.get("danger_explanation"), limit=3)
        self.guardian_simulation_advice = str(sim.get("guardian_advice", ""))

        summary = str(arch.get("danger_summary", "")).strip()
        bullets = target_object_risk_bullets(tgt) if has_target else []
        if has_target and bullets:
            joined = "；".join(bullets)
            self.guardian_interaction_framing = (
                f"與「{self.insight_target_name}」這段互動裡，這個對象可能會：{joined}。"
            )
        elif summary:
            self.guardian_interaction_framing = (
                "有些人習慣帶來「"
                + self.relationship_archetype_name
                + "」的節奏，可能會這樣耗你："
                + summary
            )
        else:
            self.guardian_interaction_framing = "你不需要自己承受所有壓力。"

        why: List[str] = []
        for m in sim.get("risk_matches", [])[:2]:
            ms = str(m).strip()
            if ms and ms not in why:
                why.append(ms)
        for line in self.guardian_why_lines:
            ls = str(line).strip()
            if ls and ls not in why and len(why) < 3:
                why.append(ls)
        if why:
            self.guardian_why_lines = why

        ux = generate_interaction_reasoning(
            profile=bundle.get("profile"),
            target_profile=tgt if has_target else None,
            inference=inf,
            relationship_simulation=sim,
            archetype=arch,
            match_score=score,
        )
        self.ux_why_drains_line = str(ux.get("why_drains", "") or "")
        self.ux_rhythm_conflict_line = str(ux.get("rhythm_conflict", "") or "")
        self.ux_pressure_bullets = _str_list(ux.get("pressure_bullets"), limit=3)
        self.ux_fit_reasoning = str(ux.get("fit_reasoning", "") or "")
        self.ux_avoid_reasoning = str(ux.get("avoid_reasoning", "") or "")
        self.ux_fox_observer_note = str(ux.get("fox_observer", "") or "")
        if self.ux_why_drains_line:
            self.energy_summary = self.ux_why_drains_line
        if self.ux_fit_reasoning:
            self.compatibility_title = self.ux_fit_reasoning
        if self.ux_fox_observer_note:
            self.fox_message = self.ux_fox_observer_note

    @rx.var(cache=True)
    def insight_target_summary_line(self) -> str:
        if not (self.insight_target_name or "").strip():
            return "尚未命名觀察對象：請先到「觀察對象」頁補上稱呼與節奏，分析會更貼近真實互動。"
        rel = (self.insight_target_relationship or "").strip()
        if rel:
            return f"分析對象：「{self.insight_target_name}」（{rel}）"
        return f"分析對象：「{self.insight_target_name}」"

    @rx.var(cache=True)
    def guardian_main_warning_title(self) -> str:
        label = (self.insight_target_name or "").strip()
        if self.display_risk_level == "high":
            if label:
                return f"與「{label}」這段互動：壓力訊號偏高"
            return "目前訊號偏危險"
        if self.display_risk_level == "medium":
            if label:
                return f"與「{label}」這段互動：節奏偏消耗"
            return "你正在進入高消耗節奏"
        if label:
            return f"與「{label}」這段互動：目前相對平穩"
        return "目前訊號相對平穩"

    @rx.var(cache=True)
    def guardian_risk_status_short(self) -> str:
        if self.display_risk_level == "high":
            return "目前有較高消耗風險"
        if self.display_risk_level == "medium":
            return "壓力訊號正在升溫"
        return "目前沒有明顯危險訊號"

    @rx.var(cache=True)
    def guardian_action_display(self) -> str:
        t = (self.guardian_action or "").strip()
        if t:
            return t
        return "先替自己保留步調與界線，必要時更新訊號資料後再跑一次分析。"

    @rx.event
    def load_session_history(self) -> None:
        hist = load_history()
        self.session_history = hist if isinstance(hist, list) else []
        self._refresh_fox_memory_from_store()

    @rx.event
    async def run_demo_match(self):
        async with self:
            self.demo_match_loading = True
        try:
            user_a = load_profile()
            tgt = load_target_profile()
            if str(tgt.get("target_name", "")).strip():
                user_b = build_virtual_partner_profile(tgt)
            else:
                user_b = {
                    "interests": ["music", "travel", "sports"],
                    "activity": 6,
                }

            result = execute_bound_flow(
                {},
                user_a,
                user_b,
            )

            async with self:
                self.flow_result = result if isinstance(result, dict) else {}
                ins = result.get("insight_state", {}) if isinstance(result, dict) else {}
                self.insight_state = ins if isinstance(ins, dict) else {}
                self._apply_emotional_insight()

                if self.insight_state:
                    score = _match_score_from_flow(self.flow_result)
                    mem = remember_insight(self.insight_state, score)
                    self.fox_memory_note = mem["guardian_memory_note"]
                    self.recurring_pattern = mem["recurring_pattern"]
                    apply_inference_memory_tags(
                        self.inference_risk_scores,
                        self.signal_inference_types,
                    )
                    record_relationship_simulation_memory(
                        self.relationship_archetype_name,
                        self.relationship_interaction_risk_score,
                    )
                    record_target_pattern_memory(
                        str(tgt.get("target_name", "")),
                        self.relationship_archetype_name,
                        self.relationship_interaction_risk_score,
                    )
                    self._refresh_fox_memory_from_store()
                    append_history(
                        {
                            "compatibility_title": self.compatibility_title,
                            "energy_summary": self.energy_summary,
                            "final_insight": self.final_insight,
                        }
                    )
                else:
                    self._refresh_fox_memory_from_store()
        finally:
            async with self:
                self.demo_match_loading = False

    @rx.event
    def load_latest_session(self) -> None:
        session = load_session()
        if not isinstance(session, dict):
            session = {}

        fr = session.get("flow_result", {})
        self.flow_result = fr if isinstance(fr, dict) else {}

        ins = session.get("insight_state", {})
        self.insight_state = ins if isinstance(ins, dict) else {}

        self._apply_emotional_insight()
        self._refresh_fox_memory_from_store()
