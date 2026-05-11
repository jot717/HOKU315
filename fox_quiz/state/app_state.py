from __future__ import annotations

from typing import Any, Dict, List

import reflex as rx

from product.app_binding.runtime.flow_binding import execute_bound_flow
from product.app_binding.runtime.persistence import load_session
from product.insight.experience.fox_narration import build_fox_message
from product.insight.experience.insight_formatter import format_emotional_insight
from product.insight.experience.reveal_engine import build_reveal_state
from product.guard.runtime.signal_guard_engine import evaluate_signal_risk
from product.memory.runtime.fox_memory_engine import remember_insight
from product.memory.runtime.fox_memory_store import get_memory_display
from product.profile.runtime.profile_store import load_profile
from product.session.runtime.session_history import append_history, load_history


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

    @rx.var(cache=True)
    def has_insight(self) -> bool:
        return bool(self.insight_state)

    @rx.var(cache=True)
    def insight_ai_summary(self) -> str:
        if not self.insight_state:
            return ""
        return str(self.insight_state.get("ai_summary", ""))

    @rx.var(cache=True)
    def insight_shared_traits_text(self) -> str:
        if not self.insight_state:
            return ""
        st = self.insight_state.get("shared_traits", [])
        if isinstance(st, list):
            return ", ".join(str(x) for x in st)
        return str(st)

    @rx.var(cache=True)
    def insight_activity_analysis(self) -> str:
        if not self.insight_state:
            return ""
        return str(self.insight_state.get("activity_analysis", ""))

    @rx.var(cache=True)
    def match_score_safe_int(self) -> int:
        """0–100 int for rx.progress (requires int, not float)."""
        s = float(self.flow_result.get("match", {}).get("score", 0))
        return max(0, min(100, int(round(s))))

    @rx.var(cache=True)
    def match_score_heading(self) -> str:
        safe = max(
            0,
            min(
                100,
                int(
                    round(
                        float(self.flow_result.get("match", {}).get("score", 0)),
                    )
                ),
            ),
        )
        return f"{safe}%"

    def _refresh_fox_memory_from_store(self) -> None:
        display = get_memory_display()
        self.fox_memory_note = str(display.get("guardian_memory_note", ""))
        self.recurring_pattern = str(display.get("recurring_pattern", ""))

    def _apply_emotional_insight(self) -> None:
        if not self.insight_state:
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
            self._refresh_fox_memory_from_store()
            return

        score = float(self.flow_result.get("match", {}).get("score", 0))
        emotional = format_emotional_insight(self.insight_state, score)
        self.compatibility_title = emotional.get("compatibility_title", "")
        self.energy_summary = emotional.get("energy_summary", "")
        self.final_insight = emotional.get("final_insight", "")

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

    @rx.event
    def load_session_history(self) -> None:
        self.session_history = load_history()
        self._refresh_fox_memory_from_store()

    @rx.event
    async def run_demo_match(self):
        async with self:
            self.demo_match_loading = True
        try:
            user_a = load_profile()

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
                self.flow_result = result
                self.insight_state = result.get(
                    "insight_state",
                    {},
                )
                self._apply_emotional_insight()

                if self.insight_state:
                    score = float(self.flow_result.get("match", {}).get("score", 0))
                    mem = remember_insight(self.insight_state, score)
                    self.fox_memory_note = mem["guardian_memory_note"]
                    self.recurring_pattern = mem["recurring_pattern"]
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

        self.flow_result = session.get(
            "flow_result",
            {},
        )

        self.insight_state = session.get(
            "insight_state",
            {},
        )
        self._apply_emotional_insight()
        self._refresh_fox_memory_from_store()
