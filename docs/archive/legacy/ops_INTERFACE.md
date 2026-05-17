# OPS LAYER INTERFACE

## Entry Points

- **TEST**:
  - **`pytest tests/regression/`** (and **`python scripts/run_regression.py`**)
  - **purpose**: protect system integrity

- **SCRIPTS**:
  - **`scripts/*`**
  - **purpose**: runtime collection + utilities

- **DOCS**:
  - **`docs/*`**
  - **purpose**: system documentation

## RULE

Ops layer is the **ONLY** cross-layer allowed dependency zone.

See also [`docs/active/governance/REPO_ARCHITECTURE.md`](../docs/active/governance/REPO_ARCHITECTURE.md), [`docs/active/governance/ARCHITECTURE_CONTRACT.md`](../docs/active/governance/ARCHITECTURE_CONTRACT.md).
