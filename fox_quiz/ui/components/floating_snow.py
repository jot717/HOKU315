from __future__ import annotations

import reflex as rx

_SNOW = [
    ("8%", "12%", 0.35),
    ("22%", "8%", 0.25),
    ("78%", "15%", 0.3),
    ("88%", "28%", 0.22),
    ("15%", "45%", 0.28),
    ("55%", "38%", 0.26),
    ("40%", "62%", 0.32),
    ("70%", "72%", 0.24),
    ("30%", "82%", 0.2),
    ("92%", "55%", 0.27),
    ("5%", "68%", 0.23),
    ("65%", "12%", 0.29),
]


def floating_snow() -> rx.Component:
    flakes: list[rx.Component] = []
    for left, top, opacity in _SNOW:
        flakes.append(
            rx.box(
                rx.text(
                    "·",
                    font_size="1.25rem",
                    color="var(--slate-4)",
                    as_="span",
                ),
                position="absolute",
                left=left,
                top=top,
                opacity=opacity,
                user_select="none",
                pointer_events="none",
                style={"text_shadow": "0 0 12px rgba(255,255,255,0.9)"},
            )
        )
    return rx.box(
        *flakes,
        position="absolute",
        inset="0",
        overflow="hidden",
        pointer_events="none",
        z_index="0",
    )
