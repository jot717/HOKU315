from __future__ import annotations

from typing import Any


def build_fox_message(insight: dict[str, Any], score: float) -> str:
    if not isinstance(insight, dict):
        return ""

    if score >= 80:
        return (
            "北極狐靜靜觀察了一會。\n"
            "你們之間的訊號很乾淨，沒有太多讓人疲憊的雜訊。"
        )

    if score >= 60:
        return (
            "北極狐注意到一些溫和的共鳴。\n"
            "但還需要更多時間確認彼此是否真的安全。"
        )

    return (
        "北極狐察覺到一些容易消耗情緒的訊號。\n"
        "也許先保留距離，會比較舒服。"
    )
