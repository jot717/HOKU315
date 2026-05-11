from __future__ import annotations

from typing import Any, Dict


def format_emotional_insight(
    insight: Dict[str, Any],
    score: float,
) -> Dict[str, str]:
    """Guardian-tone copy; dict keys unchanged for session / regression contracts."""
    if score >= 80:
        compatibility = "訊號較為清澈"
        energy = "界線清楚一些，不必急著靠近。"

    elif score >= 60:
        compatibility = "訊號還在流動"
        energy = "有些重疊，也保留著各自的形狀；慢慢觀察比較安心。"

    else:
        compatibility = "訊號顯得疲憊"
        energy = "差異帶來拉扯時，先顧好自己比較重要。"

    traits = insight.get(
        "shared_traits",
        [],
    )

    traits_text = ", ".join(str(t) for t in traits)

    if traits_text:
        final_insight = (
            f"北極狐看見你們在「{traits_text}」附近有相似的痕跡，"
            "但相似不代表一定要靠近——留一點空白，也是保護。"
        )
    else:
        final_insight = (
            "北極狐建議先從自己的節奏出發，"
            "不必急著讀懂對方；安靜觀察，本身就是守護。"
        )

    return {
        "compatibility_title": compatibility,
        "energy_summary": energy,
        "final_insight": final_insight,
    }
