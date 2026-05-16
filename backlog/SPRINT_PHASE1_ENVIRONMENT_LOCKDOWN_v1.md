# SPRINT — PHASE1-E Environment Lockdown v1

**Status:** Active until gates green on policy Python + `.venv`

## Deliverables

1. **Pins** — `reflex==0.9.2.post1`, `reflex-components-radix==0.9.2`, aligned `reflex-base` / core / code.
2. **Lock** — `requirements-lock.txt` from clean 3.11 install.
3. **Startup** — `start_hoku.bat`, `run_all_checks.bat`.
4. **Ops** — `ops/env/*.md`, sanity + compile scripts.
5. **Tests** — `tests/regression/test_phase1e_environment_lockdown_v1.py`.

## Verify

```bat
run_all_checks.bat
```

Manual: `start_hoku.bat` — app routes load, no radix import crash.

## References

- [`ops/env/STARTUP_GUIDE.md`](../ops/env/STARTUP_GUIDE.md)
- [`ops/env/DEPENDENCY_LOCK_REPORT.md`](../ops/env/DEPENDENCY_LOCK_REPORT.md)
