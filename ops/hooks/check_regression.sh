#!/usr/bin/env sh
# Regression gate (POSIX). Run from repository root.

set -e
echo "RUNNING REGRESSION GATE"

python -m pytest tests/regression/ "$@"

echo "REGRESSION PASSED"
