# Backlog

**Canonical index:** [`MASTER_BACKLOG.md`](MASTER_BACKLOG.md)  
**Product truth:** [`../ops/product/PRODUCT_MASTER.md`](../ops/product/PRODUCT_MASTER.md)  
**Engineering P0/P1:** [`../BACKLOG.md`](../BACKLOG.md)

## Structure

| Location | Contents |
|----------|----------|
| `MASTER_BACKLOG.md` | ACTIVE / COMPLETED / ARCHIVED / FUTURE — one row per phase |
| `archive/` | Historical `BACKLOG_*_v1.md` and `SPRINT_*_v1.md` slices |
| `../BACKLOG.md` | Stabilization, tasks, hotfix archive (engineering) |
| `../SPRINT_LOG.md` | Daily done/next |

## Rules

- Do **not** add a second master backlog.
- New work → one row in `MASTER_BACKLOG.md` (ACTIVE).
- When a sprint completes → move slice files to `archive/`, move row to COMPLETED.
