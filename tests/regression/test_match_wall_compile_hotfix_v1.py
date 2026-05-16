from __future__ import annotations

import inspect

from fox_quiz.match_wall import enrich_match_row_for_ui, match_wall_page


def test_enrich_match_row_buckets_from_plain_floats() -> None:
    low = enrich_match_row_for_ui({"distance": 0.2, "is_blurred": False}, 0)
    assert low["compat_bucket"] == "h"
    assert low["risk_bucket"] == "l"
    assert low["emotion_line"]
    assert low["scenario_line"]
    assert low["distance_str"] == "0.200"

    mid = enrich_match_row_for_ui({"distance": 0.5, "is_blurred": False}, 1)
    assert mid["compat_bucket"] == "m"
    assert mid["risk_bucket"] == "m"

    high_d = enrich_match_row_for_ui({"distance": 0.9, "is_blurred": False}, 2)
    assert high_d["compat_bucket"] == "l"

    blurred = enrich_match_row_for_ui({"distance": 0.5, "is_blurred": True}, 3)
    assert blurred["risk_bucket"] == "h"
    assert blurred["emotion_line"]
    assert "模糊" in blurred["emotion_line"] or "落差" in blurred["emotion_line"]


def test_match_card_renderer_has_no_distance_threshold_compare() -> None:
    from fox_quiz import match_wall as mw

    src = inspect.getsource(mw._match_card)
    for bad in ("<= 0.", "< 0.", ">= 0.", "> 0."):
        assert bad not in src, f"forbidden threshold fragment {bad!r} in _match_card"


def test_match_wall_page_builds() -> None:
    assert match_wall_page() is not None


def test_load_path_assigns_card_idx_via_enrich() -> None:
    """Regression: rows from loader must include foreach-safe keys."""
    sample = enrich_match_row_for_ui(
        {
            "distance": 0.3,
            "is_blurred": False,
            "user_id": "u1",
            "conflict_dim_label": "x",
            "image_url": "http://example.com/i.jpg",
        },
        7,
    )
    assert sample["card_idx"] == 7
    assert "compat_bucket" in sample
