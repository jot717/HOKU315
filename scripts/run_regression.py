#!/usr/bin/env python3
"""Regression gate wrapper (pytest tests/regression/). Exit code propagates."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def main() -> int:
    root = repo_root()
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/regression/", "-v", "--tb=short"],
        cwd=root,
        capture_output=False,
        text=True,
    )

    if result.returncode == 0:
        print("REGRESSION PASS - OK to proceed with manual patch apply after human review")
    else:
        print("REGRESSION FAIL - BLOCK patch merge/deploy until fixed")

    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
