"""Runtime JSON sanitation and Python/venv checks for HOKU315 (PHASE1-E)."""
from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "runtime_state"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


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


_ENTITY_BY_FILE = {
    "user_profile.json": "user_profile",
    "target_profile.json": "target_profile",
    "fox_memory.json": "fox_memory",
    "session_history.json": "session_history",
    "local_session.json": "local_session",
}


def _read_entity(rel: str) -> Any | None:
    from product.persistence.runtime import registry

    entity = _ENTITY_BY_FILE.get(rel)
    if entity is None:
        return None
    if not (RUNTIME_DIR / rel).exists():
        return None
    return registry.get_backend().read(entity)


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
    from product.session.runtime.session_history import reset_session_history

    reset_session_history()


def _fix_local_session() -> None:
    from product.app_binding.runtime.persistence import persist_session

    persist_session({})


def _valid_user_profile(o: Any) -> bool:
    from product.profile.runtime.profile_store import normalize_profile

    if not isinstance(o, dict):
        return False
    try:
        normalized = normalize_profile(o)
    except (TypeError, ValueError):
        return False
    return (
        "name" in normalized
        and "interests" in normalized
        and "activity" in normalized
        and isinstance(normalized.get("interests"), list)
        and 0 <= int(normalized.get("activity", 0)) <= 10
    )


def _valid_target_profile(o: Any) -> bool:
    from product.target.runtime.target_profile_store import normalize_target_profile

    if not isinstance(o, dict):
        return False
    try:
        normalized = normalize_target_profile(o)
    except (TypeError, ValueError):
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
    return all(k in normalized for k in required)


def _valid_fox_memory(o: Any) -> bool:
    from product.memory.runtime.fox_memory_store import normalize_fox_memory

    if not isinstance(o, dict):
        return False
    try:
        normalized = normalize_fox_memory(o)
    except (TypeError, ValueError):
        return False
    return isinstance(normalized.get("recent_patterns"), list) and isinstance(
        normalized.get("recent_warnings"),
        list,
    )


def _valid_history(o: Any) -> bool:
    from product.session.runtime.session_history import _unpack_history

    if isinstance(o, list):
        return True
    if isinstance(o, dict) and isinstance(o.get("items"), list):
        _unpack_history(o)
        return True
    return False


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
            f"(use 3.11.x or 3.12.x; see docs/active/env/PYTHON_VERSION_POLICY.md)",
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
        data = _read_entity(rel) if path.exists() else None
        if data is None and path.exists():
            data = None  # corrupt JSON treated as missing

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
