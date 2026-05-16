from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_python_version_file_exists() -> None:
    p = ROOT / ".python-version"
    assert p.is_file()
    text = p.read_text(encoding="utf-8").strip()
    assert text.startswith("3.11") or text.startswith("3.12")


def test_requirements_lock_matches_reflex_bundle() -> None:
    lock = (ROOT / "requirements-lock.txt").read_text(encoding="utf-8")
    assert "reflex==0.9.2.post1" in lock
    assert "reflex-components-radix==0.9.2" in lock


def test_ops_env_artifacts_exist() -> None:
    for rel in (
        "ops/env/PYTHON_VERSION_POLICY.md",
        "ops/env/VENV_POLICY.md",
        "ops/env/DEPENDENCY_LOCK_REPORT.md",
        "ops/env/RUNTIME_STATE_SCHEMA.md",
        "ops/env/STARTUP_GUIDE.md",
        "ops/env/CLEANUP_LOG_PHASE1E.md",
        "ops/env/runtime_sanity_check.py",
        "ops/env/reflex_compile_gate.py",
    ):
        assert (ROOT / rel).is_file(), rel


def test_startup_scripts_exist() -> None:
    assert (ROOT / "start_hoku.bat").is_file()
    assert (ROOT / "run_all_checks.bat").is_file()


def test_phase1e_backlog_sprint_docs() -> None:
    assert (ROOT / "backlog/BACKLOG_PHASE1_ENVIRONMENT_LOCKDOWN_v1.md").is_file()
    assert (ROOT / "backlog/SPRINT_PHASE1_ENVIRONMENT_LOCKDOWN_v1.md").is_file()


def test_runtime_sanity_script_runs_with_fix() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "ops" / "env" / "runtime_sanity_check.py"), "--fix"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert r.returncode == 0, r.stderr + r.stdout


def test_radix_plugin_import_when_installed() -> None:
    try:
        from reflex_components_radix.plugin import RadixThemesPlugin  # noqa: F401
    except ImportError as e:
        pytest.skip(f"Reflex radix stack not installed in this interpreter: {e}")
