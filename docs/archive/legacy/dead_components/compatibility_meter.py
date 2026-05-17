from __future__ import annotations

from typing import Union

import reflex as rx


def compatibility_meter(
    safe_score: Union[int, rx.Var],
    pct_label: Union[str, rx.Var],
) -> rx.Component:
    """Use AppState.match_score_safe_int + match_score_heading so value is int for rx.progress."""
    return rx.vstack(
        rx.heading(pct_label, size="5"),
        rx.progress(
            value=safe_score,
            max=100,
            width="100%",
        ),
        spacing="2",
        width="100%",
    )
