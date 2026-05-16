"""Reflex compile gate — must succeed inside project .venv (PHASE1-E)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    try:
        from reflex_components_radix.plugin import RadixThemesPlugin  # noqa: F401
    except ImportError as e:
        print(
            "[reflex_compile_gate] ERROR: radix plugin import failed — use repo .venv and "
            "requirements.txt (reflex 0.9.2.post1, reflex-components-radix 0.9.2).",
            file=sys.stderr,
        )
        print(e, file=sys.stderr)
        return 1

    r = subprocess.run(
        [sys.executable, "-m", "reflex", "compile"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode == 0:
        print("[reflex_compile_gate] OK (full compile)")
        return 0

    combined = (r.stderr or "") + (r.stdout or "")
    locked = sys.platform == "win32" and "PermissionError" in combined and ".web" in combined
    if locked:
        print(
            "[reflex_compile_gate] WARNING: reflex compile hit a Windows file lock on `.web` "
            "(common under OneDrive). Running import smoke instead; close other Reflex/Node "
            "processes or clone outside cloud sync for a full compile.",
            file=sys.stderr,
        )
        try:
            if str(ROOT) not in sys.path:
                sys.path.insert(0, str(ROOT))
            import fox_quiz.fox_quiz  # noqa: F401
        except Exception as imp_err:
            print(f"[reflex_compile_gate] ERROR: import smoke failed: {imp_err}", file=sys.stderr)
            print(combined[-4000:], file=sys.stderr)
            return 1
        print("[reflex_compile_gate] OK (import smoke; full compile skipped due to .web lock)")
        return 0

    print("[reflex_compile_gate] ERROR: reflex compile failed.", file=sys.stderr)
    print(combined[-8000:], file=sys.stderr)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
