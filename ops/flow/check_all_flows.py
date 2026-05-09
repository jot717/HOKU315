from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

registry_path = ROOT / "ops" / "flow" / "flow_registry.json"

with open(registry_path, encoding="utf-8") as f:
    registry = json.load(f)

required = [
    "README.md",
    "state_model.md",
    "product_flow.md",
]

failed = False

for flow in registry["flows"]:
    flow_dir = ROOT / "product" / flow

    print(f"CHECK FLOW: {flow}")

    for item in required:
        target = flow_dir / item

        if not target.exists():
            print(f"FAILED: missing {target}")
            failed = True

    runtime_dir = flow_dir / "runtime"

    if not runtime_dir.exists():
        print(f"FAILED: missing runtime dir in {flow}")
        failed = True

    regression = ROOT / "tests" / "regression" / f"test_{flow}_flow.py"

    if not regression.exists():
        print(f"FAILED: missing regression {regression}")
        failed = True

if failed:
    sys.exit(1)

print("FLOW CONSISTENCY PASSED")
