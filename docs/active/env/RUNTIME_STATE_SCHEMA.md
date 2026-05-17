# Runtime state schema — `runtime_state/`

Local JSON used by **profile**, **target**, **session binding**, **insight history**, and **fox memory**. Paths are relative to repo root.

These files are the **Phase 1 / Phase 2-A local runtime** contract. All reads/writes go through `product/persistence/runtime/` (`HOKU_PERSISTENCE_BACKEND=local`).

Phase 2-B+ may add cloud backends; schema keys remain stable.

| File | Purpose | Schema (normative) |
|------|---------|---------------------|
| `user_profile.json` | Baseline signal profile | `name` (string), `interests` (string array), `activity` (int 1–10) — see `product/profile/runtime/profile_store.py` |
| `target_profile.json` | Observed person / context | See `DEFAULT_TARGET` in `product/target/runtime/target_profile_store.py` |
| `local_session.json` | App flow binding session blob | Arbitrary JSON object; empty `{}` if absent — `product/app_binding/runtime/persistence.py` |
| `session_history.json` | Last N insight rows | JSON array of objects with string fields `compatibility_title`, `energy_summary`, `final_insight` |
| `fox_memory.json` | Rule-based memory display | `recent_patterns`, `recent_warnings` (arrays), `last_guardian_note`, `last_seen_energy`, `updated_at` (strings) — `DEFAULT_MEMORY` in `product/memory/runtime/fox_memory_store.py` |

## Recovery

- **`ops/env/runtime_sanity_check.py --fix`** rewrites corrupted or invalid JSON to **safe defaults** (and ensures the directory exists).
- Product code paths (`load_profile`, `load_target_profile`, etc.) may also heal some fields on read.

## Git / hygiene

`.gitignore` excludes local copies of several of these to avoid committing machinespecific state; **schema** still applies when files exist.

See [`STARTUP_GUIDE.md`](STARTUP_GUIDE.md).
