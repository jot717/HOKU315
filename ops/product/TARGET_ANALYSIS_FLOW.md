# TARGET ANALYSIS FLOW (v1)

This is the **primary product loop** (documentation contract; implementation follows in UI + stores).

## Canonical UX path

```
HOME
  → PROFILE (user signal profile)
  → TARGET SETUP (/target — observation entity)
  → INSIGHT (/insight — run observation)
  → FOX GUARDIAN OUTPUT (target-aware + user vs archetype overlap)
  → MEMORY (recurring patterns / target tags)
```

Users may skip optional `/quiz` (mine sliders) when not needed; **target setup** is the step that removes "abstract guardian" by naming **who** is being observed in signal terms.

## Out of scope (v1)

- Real SNS ingestion
- Multi-user backend
- Auth-gated cloud target store

## References

- [`TARGET_SIGNAL_CONSTITUTION.md`](TARGET_SIGNAL_CONSTITUTION.md)
- [`TARGET_PROFILE_SCHEMA.md`](TARGET_PROFILE_SCHEMA.md)
- Runtime: `product/target/runtime/target_profile_store.py`
- Simulation: `product/signal/runtime/relationship_simulation_engine.py`
