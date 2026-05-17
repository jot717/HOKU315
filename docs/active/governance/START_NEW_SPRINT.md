# START NEW SPRINT

## PURPOSE

Mandatory AI boot sequence. **No implementation before load.**

---

## Canonical SSOT loading order

Load in order; never skip:

| Step | File |
|------|------|
| 1 | [`README.md`](../../../README.md) |
| 2 | [`docs/README.md`](../../README.md) |
| 3 | [`docs/active/governance/SSOT_HIERARCHY.md`](SSOT_HIERARCHY.md) |
| 4 | [`docs/active/product/PRODUCT_MASTER.md`](../product/PRODUCT_MASTER.md) |
| 5 | [`docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md`](../product/AI_DEVELOPMENT_CONSTITUTION.md) |
| 6 | [`docs/active/product/ROADMAP.md`](../product/ROADMAP.md) |
| 7 | [`GOVERNANCE_CHECKLIST.md`](GOVERNANCE_CHECKLIST.md) |
| 8 | [`MASTER_BACKLOG.md`](MASTER_BACKLOG.md) |

Optional before coding: domain SSOT (`SIGNAL_SYSTEM`, `MATCH_SYSTEM`, `ACTIVE_SURFACE_MAP`), sprint slice from `backlog/archive/`.

---

## Authority ownership

| Concern | Owner |
|---------|--------|
| **Roadmap / phases** | [`ROADMAP.md`](../product/ROADMAP.md) — PHASE1–PHASE7 only |
| **Planning / what is ACTIVE** | [`MASTER_BACKLOG.md`](MASTER_BACKLOG.md) |
| **Engineering P0/P1** | Root [`BACKLOG.md`](../../../BACKLOG.md) — not phase law |
| **Sprint slice detail** | `backlog/archive/BACKLOG_*` + `SPRINT_*` |
| **Sprint execution boot** | This file + [`AI_TASK_TEMPLATE.md`](AI_TASK_TEMPLATE.md) |
| **Implementation rules** | [`AI_DEVELOPMENT_CONSTITUTION.md`](../product/AI_DEVELOPMENT_CONSTITUTION.md) |
| **Precedence map** | [`SSOT_HIERARCHY.md`](SSOT_HIERARCHY.md) |

---

## Implementation authority chain

```
ROADMAP (phase law)
  → MASTER_BACKLOG (ACTIVE row)
    → BACKLOG/SPRINT slice (backlog/archive/)
      → IMPLEMENT (docs/active + code)
        → REGRESSION
          → UAT
            → DONE
              → ARCHIVE
```

Never skip phases. Never implement from archive.

---

## Archive usage rules

| Allowed | Forbidden |
|---------|-----------|
| Post-completion historical reference | Phase inference from `FOX_ROADMAP`, old constitutions |
| Moving completed slices to `backlog/archive/` | ACTIVE rows only in archive |
| Reading `SPRINT_LOG_FULL` for history | Using archive UAT as acceptance law |

**Archive never overrides** `docs/active/product/` or `docs/active/governance/`.

---

## FORBIDDEN AI BEHAVIORS

* create parallel constitutions or v2/v3 architecture docs  
* create duplicate roadmap files  
* infer PHASE6/7 (or any phase) from archive  
* create root markdown files  
* mix product PHASE2+ into Phase 1 face  
* bypass regression or UAT  
* put product truth in `ops/`  

---

## REPO DISCIPLINE

**Root:** entry only — `README.md`, `BACKLOG.md`, `SPRINT_LOG.md`, requirements, scripts/config.

**docs/active/:** single knowledge layer.  
**docs/archive/:** historical only.  
**ops/:** `env`, `flow`, `debug`, `testing` executables only.

---

## PRODUCT TRUTH (extend in place only)

* `PRODUCT_MASTER.md`  
* `SIGNAL_SYSTEM.md`  
* `MATCH_SYSTEM.md`  
* `ROADMAP.md`  

Phase detail: **PHASE1–PHASE7** in `ROADMAP.md` only. Never implement future phases early.
