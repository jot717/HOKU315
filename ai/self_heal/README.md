# Self-healing loop v1 (SAFE MODE)

**No auto-deploy.** Outputs JSON for human review; regression must pass before any manual code change.

| Step | Command |
|------|---------|
| Suggest + patch file | `python -m ai.self_heal.suggest_bridge STATE_DESYNC` |
| Manual suggestion | `python -m ai.self_heal.patch_engine STATE_DESYNC "your suggestion"` |
| Review printout | `python -m ai.self_heal.apply_patch --patch ai/self_heal/patches/STATE_DESYNC.json` |
| Regression gate | `python scripts/run_regression.py` |
| Log outcome | `python -m ai.self_heal.learning_log STATE_DESYNC --success` |

See [`BACKLOG.md`](../../BACKLOG.md) **SELF-HEALING SYSTEM v1** and [`docs/AI_PATCH_FLOW.md`](../../docs/AI_PATCH_FLOW.md).
