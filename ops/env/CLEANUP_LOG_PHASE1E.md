# PHASE1-E cleanup log

**Phase:** Environment Lockdown v1  
**Date:** 2026-05-16

## Dependency alignment

- Bumped **Reflex** / **reflex-base** to **0.9.2.post1** and **reflex-components-radix** (plus matching core packages) to resolve missing **`reflex_components_radix.plugin`** on import (root cause of compile failure when radix stayed on 0.9.1).
- Regenerated **`requirements-lock.txt`** from a clean Python **3.11** install as **UTF-8** (no UTF-16 BOM; avoid PowerShell `>` redirect for freeze output).
- **`reflex_compile_gate.py`**: on Windows `.web` **PermissionError** (e.g. OneDrive), falls back to radix import + **`fox_quiz`** import smoke with repo root on `sys.path`; prefer full compile when locks are cleared.

## Removed / avoided

- Dropped reliance on **global Python 3.14** (and other non-policy interpreters) for Reflex compile in docs and gates; policy directs developers to **`.venv`** + **3.11/3.12**.

## Temporary artifacts (do not commit)

- Local-only **`venv/`**, **`.venv_lock_gen/`**, **`.venv_phase1e_check/`**, **`.venv_ci/`** (if recreated) — delete after use.

## Follow-up (out of scope for PHASE1-E)

- PHASE1-D / PHASE1-F / PHASE2 per master plan (do not start until prior phase closed).
