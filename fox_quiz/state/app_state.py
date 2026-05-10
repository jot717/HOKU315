from __future__ import annotations

from typing import Any, Dict

import reflex as rx

from product.app_binding.runtime.flow_binding import execute_bound_flow
from product.app_binding.runtime.persistence import load_session
from product.insight.experience.insight_formatter import format_emotional_insight


class AppState(rx.State):
    flow_result: Dict[str, Any] = {}
    insight_state: Dict[str, Any] = {}

    compatibility_title: str = ""
    energy_summary: str = ""
    final_insight: str = ""

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

    def _apply_emotional_insight(self) -> None:
        if not self.insight_state:
            self.compatibility_title = ""
            self.energy_summary = ""
            self.final_insight = ""
            return
        score = float(self.flow_result.get("match", {}).get("score", 0))
        emotional = format_emotional_insight(self.insight_state, score)
        self.compatibility_title = emotional.get("compatibility_title", "")
        self.energy_summary = emotional.get("energy_summary", "")
        self.final_insight = emotional.get("final_insight", "")

    @rx.event
    def run_demo_match(self) -> None:
        user_a = {
            "interests": ["ai", "music", "travel"],
            "activity": 5,
        }

        user_b = {
            "interests": ["music", "travel", "sports"],
            "activity": 6,
        }

        result = execute_bound_flow(
            {},
            user_a,
            user_b,
        )

        self.flow_result = result
        self.insight_state = result.get(
            "insight_state",
            {},
        )
        self._apply_emotional_insight()

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
