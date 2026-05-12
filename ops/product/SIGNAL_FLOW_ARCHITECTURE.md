# SIGNAL FLOW ARCHITECTURE (v1)

**STATUS:** ACTIVE consolidation map  
**Scope:** Describes **real routes and artifacts** today + **planned** extensions. No new backend in this sprint.

Aligned with [`SIGNAL_SYSTEM_CONSTITUTION.md`](SIGNAL_SYSTEM_CONSTITUTION.md) — **no second onboarding system**.

---

## REAL FLOW (user journey)

```
Home
  →  Signal Profile Setup   (/profile)
  →  Signal Questions       (/quiz — optional depth, 20 sliders)
  →  Guardian Observation   (/insight)
  →  Signal Memory          (runtime_state/fox_memory.json + session history)
  →  Future SNS Mapping     (see SOCIAL_SIGNAL_ARCHITECTURE.md)
  →  Future Social Graph    (see CORE_PRODUCT_REALIGNMENT.md / roadmap Phase 4+)
```

**Canonical order for messaging:** profile first (portable signal file), then optional quiz for mine-dimension vector, then observation. Users may skip quiz in demo paths; copy must not imply quiz is mandatory for “having a profile.”

---

## INPUT LAYER

### Existing (shipped paths)

| Input | Where | Notes |
|-------|--------|------|
| Profile (name, interests, stress/activity) | `/profile`, `ProfileState` → `user_profile.json` | **Canonical** Signal Profile Setup |
| 20 slider “social mine” questions | `/quiz`, `QuizState.scores` → vector | **Signal questions**, not personality labels in UX |
| Demo peer / bound flow inputs | `AppState.run_demo_match` | Observation without SNS |
| Stress / activity | Profile `activity` 1–10 | Maps to `interaction_tolerance` / pressure in schema |

### Future (documented only)

* Image / card selection for quick signal probes
* SNS ingestion (opt-in)
* Social graph edges (contacts, mutes, blocks metadata)

---

## OUTPUT LAYER

### Current

* Guardian warnings and action lines (`evaluate_signal_risk`, `AppState`)
* Fox memory notes and recurring companion lines (`fox_memory_store`, `remember_insight`)
* Risk flags and level for UI chips / callouts
* Insight dict fields (`ai_summary`, `shared_traits`, `activity_analysis`) — **legacy English strings** from engine; guardian UI should continue to **frame** outputs as signal/drain, not therapy (see deprecated language doc)

### Future

* Hater / dangerous interaction alerts (policy-gated)
* Safe-circle recommendations
* Guardian network protection (graph-aware)

---

## Anti-patterns (flow)

* Introducing **`/onboarding-v2`** (or similar) that re-asks what `/profile` already captures.
* Presenting `/quiz` as a separate “product” instead of **deeper signal questions** on the same arc.
* Ending `/profile` without a **clear next step** to observation (already mitigated in profile success CTA).
