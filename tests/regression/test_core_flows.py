"""
Regression gate for core flows.

Reflex exposes HTML pages (GET), not REST POST handlers like /match with JSON body.
When REGRESSION_HTTP=1 and the app is running, we smoke-test active Phase1 GET routes.

Always-on gates (no server): reflex compile + python -m tests.run_all_tests.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
import requests

ROOT = Path(__file__).resolve().parents[2]
BASE_URL = os.environ.get("REGRESSION_BASE_URL", "http://127.0.0.1:8000")
_HTTP = os.environ.get("REGRESSION_HTTP", "") == "1"


def test_reflex_compile_gate() -> None:
    gate = ROOT / "ops" / "env" / "reflex_compile_gate.py"
    r = subprocess.run(
        [sys.executable, str(gate)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=900,
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_run_all_tests_gate() -> None:
    r = subprocess.run(
        [sys.executable, "-m", "tests.run_all_tests"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=900,
    )
    assert r.returncode == 0, r.stdout + r.stderr


@pytest.mark.skipif(not _HTTP, reason="Set REGRESSION_HTTP=1 with reflex run (see tests/regression/README.md)")
def test_match() -> None:
    res = requests.get(f"{BASE_URL}/match", timeout=120)
    assert res.status_code == 200


@pytest.mark.skipif(not _HTTP, reason="Set REGRESSION_HTTP=1 with reflex run (see tests/regression/README.md)")
def test_insight() -> None:
    res = requests.get(f"{BASE_URL}/insight", timeout=120)
    assert res.status_code == 200


@pytest.mark.skipif(not _HTTP, reason="Set REGRESSION_HTTP=1 with reflex run (see tests/regression/README.md)")
def test_profile() -> None:
    res = requests.get(f"{BASE_URL}/profile", timeout=120)
    assert res.status_code == 200
