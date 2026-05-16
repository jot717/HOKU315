"""Runtime JSON sanitation and Python/venv checks for HOKU315 (PHASE1-E)."""
from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "runtime_state"


def _supported_python() -> tuple[bool, str]:
    v = sys.version_info
    if v.major == 3 and v.minor in (11, 12):
        return True, f"{v.major}.{v.minor}.{v.micro}"
    return False, f"{v.major}.{v.minor}.{v.micro}"


def _in_repo_venv() -> bool:
    exe = Path(sys.executable).resolve()
    try:
        exe.relative_to((ROOT / ".venv").resolve())
        return True
    except ValueError:
        return False


def _load_json(path: Path) -> Any | None:
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _fix_user_profile() -> None:
    from product.profile.runtime.profile_store import DEFAULT_PROFILE, save_profile

    save_profile(dict(DEFAULT_PROFILE))


def _fix_target_profile() -> None:
    from product.target.runtime.target_profile_store import DEFAULT_TARGET, save_target_profile

    save_target_profile(dict(DEFAULT_TARGET))


def _fix_fox_memory() -> None:
    from product.memory.runtime.fox_memory_store import DEFAULT_MEMORY, save_fox_memory

    save_fox_memory(dict(DEFAULT_MEMORY))


def _fix_session_history() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    path = RUNTIME_DIR / "session_history.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump([], f, indent=2, ensure_ascii=False)


def _fix_local_session() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    path = RUNTIME_DIR / "local_session.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump({}, f, indent=2, ensure_ascii=False)


def _valid_user_profile(o: Any) -> bool:
    if not isinstance(o, dict):
        return False
    if "name" not in o or "interests" not in o or "activity" not in o:
        return False
    if not isinstance(o.get("interests"), list):
        return False
    try:
        a = int(o.get("activity", 0))
    except (TypeError, ValueError):
        return False
    return 0 <= a <= 10


def _valid_target_profile(o: Any) -> bool:
    if not isinstance(o, dict):
        return False
    required = (
        "target_name",
        "relationship_type",
        "observed_traits",
        "communication_style",
        "social_patterns",
        "pressure_signals",
        "instability_level",
        "attention_demand",
        "response_consistency",
        "notes",
    )
    if not all(k in o for k in required):
        return False
    for key in ("observed_traits", "communication_style", "social_patterns", "pressure_signals"):
        if not isinstance(o.get(key), list):
            return False
    return True


def _valid_fox_memory(o: Any) -> bool:
    if not isinstance(o, dict):
        return False
    return isinstance(o.get("recent_patterns"), list) and isinstance(
        o.get("recent_warnings"),
        list,
    )


def _valid_history(o: Any) -> bool:
    return isinstance(o, list)


def _valid_local_session(o: Any) -> bool:
    return isinstance(o, dict)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Runtime state + env sanity checks")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Rewrite broken or missing runtime_state JSON to defaults",
    )
    parser.add_argument(
        "--strict-venv",
        action="store_true",
        help="Fail if sys.executable is not under repo .venv",
    )
    args = parser.parse_args(argv)

    ok, ver = _supported_python()
    if not ok:
        print(
            f"[runtime_sanity_check] WARNING: Python {ver} is outside policy "
            f"(use 3.11.x or 3.12.x; see ops/env/PYTHON_VERSION_POLICY.md)",
            file=sys.stderr,
        )

    if args.strict_venv and not _in_repo_venv():
        print(
            "[runtime_sanity_check] ERROR: not running in repo .venv (--strict-venv). "
            "Activate .venv or run start_hoku.bat first.",
            file=sys.stderr,
        )
        return 1

    checks: tuple[tuple[str, Callable[[Any], bool], Callable[[], None]], ...] = (
        ("user_profile.json", _valid_user_profile, _fix_user_profile),
        ("target_profile.json", _valid_target_profile, _fix_target_profile),
        ("fox_memory.json", _valid_fox_memory, _fix_fox_memory),
        ("session_history.json", _valid_history, _fix_session_history),
        ("local_session.json", _valid_local_session, _fix_local_session),
    )

    problems: list[str] = []

    for rel, validate, fix in checks:
        path = RUNTIME_DIR / rel
        data = _load_json(path) if path.exists() else None

        if data is None:
            if path.exists():
                problems.append(f"{rel}: invalid JSON")
                if args.fix:
                    fix()
            elif args.fix:
                fix()
            continue

        if not validate(data):
            problems.append(f"{rel}: schema invalid")
            if args.fix:
                fix()

    if problems and not args.fix:
        for p in problems:
            print(f"[runtime_sanity_check] {p}", file=sys.stderr)
        print("[runtime_sanity_check] Re-run with --fix to repair.", file=sys.stderr)
        return 1

    print("[runtime_sanity_check] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
