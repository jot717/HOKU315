# SIGNAL SYSTEM — Single Source of Truth

> **Authority:** [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) · **Implementation:** `product/signal/`, `product/profile/`, `product/target/`, `fox_quiz/state/app_state.py`

Rule-based **social signal** pipeline only (Phase 1). No LLM inference in product face.

---

## Scope

| Surface | Route | Runtime |
|---------|-------|---------|
| Signal profile | `/profile` | `product/profile/runtime/profile_store.py` |
| Mine questionnaire | `/quiz` | `fox_logic.py`, `QuizState` |
| Target observation | `/target` | `product/target/runtime/target_profile_store.py` |
| Guardian observation | `/insight` | `infer_signal_risks`, `ux_intelligence_engine`, `relationship_simulation_engine` |

**Official flow order:** `/` → `/profile` → `/quiz` → `/target` → `/insight` → `/match` (see PRODUCT_MASTER).

---

## Core rules

1. **One onboarding path** — `/profile` + `/quiz`; no second wizard.
2. **Signal profile, not personality typing** — sliders and local fields describe interaction sensitivity.
3. **Interaction pressure** — `INTERACTION_PRESSURE_ONTOLOGY` logic lives in `ux_intelligence_engine.py` (annex: `docs/archive/product/`).
4. **Inference** — `signal_inference_engine.infer_signal_risks` combines profile, mine vector, memory, match score.
5. **Fox** — max one observer block on `/insight`; see [`CANONICAL_TERMINOLOGY.md`](CANONICAL_TERMINOLOGY.md).

---

## Artifacts

| Store | Path |
|-------|------|
| User profile | `runtime_state/user_profile.json` |
| Target profile | `runtime_state/target_profile.json` |
| Fox memory | `runtime_state/fox_memory.json` |
| Session history | `product/session/runtime/session_history.py` |

---

## Historical technical annex

Detailed constitutions and ontologies (reference-only, **not** product law):

`docs/archive/product/` — e.g. signal constitution, risk ontology, target schema, relationship models.

Do not add new parallel docs in `ops/product/`; extend this file or archive annex.
