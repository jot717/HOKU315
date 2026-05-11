from __future__ import annotations

from product.insight.experience.fox_narration import build_fox_message


def test_fox_presence_message() -> None:
    result = build_fox_message(
        {"shared_traits": ["quiet"]},
        82.0,
    )

    assert isinstance(result, str)
    assert len(result) > 0
