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

See also [`REPO_ARCHITECTURE.md`](../REPO_ARCHITECTURE.md), [`ARCHITECTURE_CONTRACT.md`](../ARCHITECTURE_CONTRACT.md).
