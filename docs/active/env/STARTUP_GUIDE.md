# Startup guide — HOKU315 (PHASE1-E)

## One-command dev server (Windows)

From repo root:

```bat
start_hoku.bat
```

This script:

1. Ensures **Python 3.11** (or **3.12**) via `py`.
2. Creates **`.venv`** if missing.
3. `pip install -r requirements.txt`
4. Runs **`python ops\env\runtime_sanity_check.py --fix`**
5. Starts **`python -m reflex run`**

### Clean terminal

- Run from **cmd** or **PowerShell**; avoid nesting multiple `activate` layers.
- Prefer repo root as cwd so `runtime_state/` resolves correctly.

## Full check suite (before merge)

```bat
run_all_checks.bat
```

Runs: **runtime sanity** (strict venv) → **Reflex compile gate** → **`pytest tests/regression/`** → **`python -m tests.run_all_tests`**.

## Reflex compile / `.web` on Windows + OneDrive

If `reflex compile` fails with **`PermissionError`** under `.web\`:

1. Stop other Reflex / Node processes.
2. Delete `.web` manually when no handles are open.
3. Prefer working copy outside **OneDrive**, or pause sync during compile (cloud folders lock files aggressively).

`ops/env/reflex_compile_gate.py` tries a **full** `reflex compile` first. On **Windows**, if `.web` is locked (typical under OneDrive), it falls back to an **import smoke** (`fox_quiz.fox_quiz`) after verifying the radix plugin — the process still exits **0**, but you should clear the lock for real CI/production builds.

## Radix / compile import errors

If you see **`No module named 'reflex_components_radix.plugin'`**:

- Use **`.venv`** only (**[`VENV_POLICY.md`](VENV_POLICY.md)**).
- Confirm pins per [`DEPENDENCY_LOCK_REPORT.md`](DEPENDENCY_LOCK_REPORT.md) (`reflex` **0.9.2.post1**, `reflex-components-radix` **0.9.2**).

## References

- [`PYTHON_VERSION_POLICY.md`](PYTHON_VERSION_POLICY.md)
- [`RUNTIME_STATE_SCHEMA.md`](RUNTIME_STATE_SCHEMA.md)
