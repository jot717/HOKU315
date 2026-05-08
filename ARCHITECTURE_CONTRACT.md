# SYSTEM ARCHITECTURE CONTRACT v1

Normative boundaries for **PRODUCT**, **AI**, and **OPS**. Companion to [`REPO_ARCHITECTURE.md`](REPO_ARCHITECTURE.md) and per-layer [`product/INTERFACE.md`](product/INTERFACE.md), [`ai/INTERFACE.md`](ai/INTERFACE.md), [`ops/INTERFACE.md`](ops/INTERFACE.md).

---

## 1. PRODUCT LAYER

- Handles user-facing logic and application routes (`fox_quiz`, shared services such as `db_service.py` as agreed in repo docs).
- **Must NOT** access AI internal modules (`import ai.*` from product UI/business code).

---

## 2. AI LAYER

- Handles debugging, taxonomy, replay mock, suggestions, and safe self-heal placeholders.
- **Must NOT** modify product logic directly via automated apply; **must NOT** depend on concrete UI components.

---

## 3. OPS LAYER

- Handles testing, CI, scripts, and documentation orchestration (paths under repo root: `tests/`, `scripts/`, `docs/`, `.github/`).
- **Allowed** to invoke workflows that touch any layer only through documented entry points (tests, scripts, CI).

---

## DATA FLOW (conceptual)

```text
product → ops (validate) → ai (analyze / suggest) → ops (regression) → product (human-applied change)
```

---

## RULE OF STABILITY

No layer may **silently** modify another layer without **ops/test validation** (e.g. **`pytest tests/regression/`**, review, and merge process per [`BACKLOG.md`](BACKLOG.md)).
