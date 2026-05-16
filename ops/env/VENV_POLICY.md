# Virtual environment policy — HOKU315 (PHASE1-E)

## Rule

All **local development**, **Reflex compile**, and **regression gates** that touch Reflex MUST use the **repository virtual environment** at:

**`%REPO_ROOT%\.venv\`**

(not the global `python`, not Microsoft Store Python, not conda base unless explicitly documented as an exception).

## Why

- Pins **exact transitive dependencies** via `requirements-lock.txt`.
- Avoids **`reflex_components_radix.plugin` / radix split** mismatches between global site-packages and this repo.
- Reduces **hydration** and **socket** weirdness from mixed package versions.

## Create / update

1. Run **`start_hoku.bat`** from the repo root (creates `.venv`, installs deps, runs sanity).
2. Or manually:
   ```bat
   py -3.11 -m venv .venv
   .venv\Scripts\activate
   python -m pip install -U pip
   pip install -r requirements.txt
   ```

## CI / automation

- Activate `.venv` (or recreate from `requirements.txt` + optional lock) before `python ops/env/reflex_compile_gate.py` and `pytest`.

## Optional strict mode

`python ops/env/runtime_sanity_check.py --strict-venv` exits non-zero if `sys.executable` is not under `.venv` (used by `run_all_checks.bat`).

See [`STARTUP_GUIDE.md`](STARTUP_GUIDE.md).
