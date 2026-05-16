from __future__ import annotations

from typing import Any


def build_fox_message(insight: dict[str, Any], score: float) -> str:
    """Legacy hook; prefer ux_intelligence_engine fox_observer for Phase1-D."""
    if not isinstance(insight, dict):
        return ""

    if score >= 80:
        return (
            "我注意到：互動裡雜訊不多，你不必為了維持熱度而多付一輪力氣。"
        )

    if score >= 60:
        return (
            "我注意到：有共鳴，但節奏仍需時間對齊——先觀察再加深會比較省電。"
        )

    return (
        "我注意到：壓力多半來自節奏與回覆期待，而不是你「做錯了什麼」。"
    )
