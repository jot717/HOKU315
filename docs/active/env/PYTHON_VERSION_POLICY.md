# Python version policy — HOKU315 (PHASE1-E)

## Supported runtimes

| Tier | Versions | Use |
|------|-----------|-----|
| **Primary** | **3.11.x** | Default DevOps and local `.venv` (matches `.python-version`). |
| **Secondary** | **3.12.x** | Allowed when 3.11 is unavailable; re-run `pip install -r requirements.txt` and lock refresh. |

## Unsupported for this repo (until explicitly reopened)

- **Python 3.13+** and **3.14+** — not validated with the pinned Reflex stack; the Windows `py` launcher may point here and break `reflex compile` or radix plugin imports.

## Enforcement

- **`.python-version`** pins **3.11.9** for pyenv/asdf-style managers (patch line may be adjusted per patch releases; stay on **3.11** minor).
- **`start_hoku.bat`** creates the venv with `py -3.11` first, then `py -3.12` if 3.11 is missing.
- **`ops/env/runtime_sanity_check.py`** warns on unsupported `sys.version_info`.

## Refresh procedure

After changing Python minor:

1. Delete `.venv`, recreate with `start_hoku.bat`.
2. `pip install -r requirements.txt`
3. Regenerate `requirements-lock.txt`: `pip freeze > requirements-lock.txt` (from the activated venv).

See also [`VENV_POLICY.md`](VENV_POLICY.md).
