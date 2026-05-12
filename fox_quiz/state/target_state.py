from __future__ import annotations

import reflex as rx

from product.target.runtime.target_profile_store import (
    load_target_profile,
    parse_comma_list,
    save_target_profile,
)

TARGET_SAVE_OK = "已儲存觀察對象。北極狐會在觀察室把你的訊號與這份觀察一起解讀。"


class TargetState(rx.State):
    target_name: str = ""
    relationship_type: str = ""
    observed_traits_text: str = ""
    communication_style_text: str = ""
    social_patterns_text: str = ""
    pressure_signals_text: str = ""
    instability_level: int = 3
    attention_demand: int = 3
    response_consistency: int = 5
    notes: str = ""
    status_message: str = ""

    @rx.event
    def sync_from_disk(self) -> None:
        t = load_target_profile()
        self.status_message = ""
        self.target_name = str(t.get("target_name", ""))
        self.relationship_type = str(t.get("relationship_type", ""))
        self.observed_traits_text = ", ".join(str(x) for x in (t.get("observed_traits") or []) if x)
        self.communication_style_text = ", ".join(
            str(x) for x in (t.get("communication_style") or []) if x
        )
        self.social_patterns_text = ", ".join(str(x) for x in (t.get("social_patterns") or []) if x)
        self.pressure_signals_text = ", ".join(str(x) for x in (t.get("pressure_signals") or []) if x)
        self.instability_level = int(t.get("instability_level", 0) or 0)
        self.attention_demand = int(t.get("attention_demand", 0) or 0)
        self.response_consistency = int(t.get("response_consistency", 5) or 5)
        self.notes = str(t.get("notes", ""))

    @rx.event
    def set_target_name(self, value: str) -> None:
        self.target_name = value

    @rx.event
    def set_relationship_type(self, value: str) -> None:
        self.relationship_type = value

    @rx.event
    def set_observed_traits_text(self, value: str) -> None:
        self.observed_traits_text = value

    @rx.event
    def set_communication_style_text(self, value: str) -> None:
        self.communication_style_text = value

    @rx.event
    def set_social_patterns_text(self, value: str) -> None:
        self.social_patterns_text = value

    @rx.event
    def set_pressure_signals_text(self, value: str) -> None:
        self.pressure_signals_text = value

    @rx.event
    def set_notes(self, value: str) -> None:
        self.notes = value

    @rx.event
    def set_instability_level(self, value: list[float | int] | float | int) -> None:
        if isinstance(value, (list, tuple)) and value:
            self.instability_level = max(0, min(10, int(round(float(value[0])))))
        else:
            self.instability_level = max(0, min(10, int(round(float(value)))))

    @rx.event
    def set_attention_demand(self, value: list[float | int] | float | int) -> None:
        if isinstance(value, (list, tuple)) and value:
            self.attention_demand = max(0, min(10, int(round(float(value[0])))))
        else:
            self.attention_demand = max(0, min(10, int(round(float(value)))))

    @rx.event
    def set_response_consistency(self, value: list[float | int] | float | int) -> None:
        if isinstance(value, (list, tuple)) and value:
            self.response_consistency = max(0, min(10, int(round(float(value[0])))))
        else:
            self.response_consistency = max(0, min(10, int(round(float(value)))))

    @rx.event
    def save_target(self) -> None:
        profile = {
            "target_name": self.target_name.strip(),
            "relationship_type": self.relationship_type.strip(),
            "observed_traits": parse_comma_list(self.observed_traits_text),
            "communication_style": parse_comma_list(self.communication_style_text),
            "social_patterns": parse_comma_list(self.social_patterns_text),
            "pressure_signals": parse_comma_list(self.pressure_signals_text),
            "instability_level": self.instability_level,
            "attention_demand": self.attention_demand,
            "response_consistency": self.response_consistency,
            "notes": self.notes.strip(),
        }
        save_target_profile(profile)
        t = load_target_profile()
        self.target_name = str(t.get("target_name", ""))
        self.relationship_type = str(t.get("relationship_type", ""))
        self.observed_traits_text = ", ".join(str(x) for x in (t.get("observed_traits") or []) if x)
        self.communication_style_text = ", ".join(
            str(x) for x in (t.get("communication_style") or []) if x
        )
        self.social_patterns_text = ", ".join(str(x) for x in (t.get("social_patterns") or []) if x)
        self.pressure_signals_text = ", ".join(str(x) for x in (t.get("pressure_signals") or []) if x)
        self.instability_level = int(t.get("instability_level", 0) or 0)
        self.attention_demand = int(t.get("attention_demand", 0) or 0)
        self.response_consistency = int(t.get("response_consistency", 5) or 5)
        self.notes = str(t.get("notes", ""))
        self.status_message = TARGET_SAVE_OK
