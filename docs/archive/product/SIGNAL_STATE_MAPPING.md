# SIGNAL STATE MAPPING (v1)

**STATUS:** Documentation only — **no major state refactor** this sprint  
**Purpose:** Map **existing** `fox_quiz/state` (and quiz state colocated in `fox_quiz.py`) to **canonical signal meaning** from [`SIGNAL_PROFILE_SCHEMA.md`](SIGNAL_PROFILE_SCHEMA.md).

---

## `ProfileState` (`fox_quiz/state/profile_state.py`)

| Field | Canonical signal bucket | Notes |
|-------|-------------------------|------|
| `name` | `identity_signals` (display) | Not a psychological label — addressability only. |
| `interests_text` / parsed `interests` | `identity_signals` + input to dyadic insight | Self-declared topic signals. |
| `activity_text` / numeric `activity` | `pressure_triggers`, `interaction_tolerance` | 1–10 self-reported stress/capacity; feeds flow as “activity”. |
| `status_message` | UX only | Not part of signal schema. |

---

## `AppState` (`fox_quiz/state/app_state.py`)

| Field / var | Canonical signal bucket | Notes |
|-------------|-------------------------|------|
| `flow_result` | `signal_history` (raw run payload) | Match score + structured results. |
| `insight_state` | `social_drain_signals`, `unsafe_interaction_patterns` (derived) | Dict from `insight_engine`: traits, activity note, summary. |
| `signal_risk_level`, `signal_risk_flags` | `unsafe_interaction_patterns`, `social_drain_signals` | Primary **risk** UX input. |
| `guardian_warning`, `guardian_action` | `guardian_notes` (latest run) | User-facing protection strings. |
| `fox_memory_note`, `recurring_pattern` | `guardian_notes`, `safe_patterns` / drain contrast | From `get_memory_display()`. |
| `compatibility_title`, `energy_summary`, `final_insight` | **Legacy naming** → interpret as **signal headlines** in product copy only | Rename deferred; emotionally “compatibility” is deprecated in outward language. |
| `fox_message` | `guardian_notes` | Narration from `build_fox_message`. |
| `session_history` | `signal_history` (append-only summaries) | Partial mirror of schema bucket. |
| `has_insight`, `insight_*` @rx.var | Projection of `insight_state` | Convenience accessors. |

---

## `QuizState` (`fox_quiz/fox_quiz.py`, not under `state/`)

| Field | Canonical signal bucket | Notes |
|-------|-------------------------|------|
| `scores` (20 × 0–1) | `hater_sensitivity`, `pressure_triggers`, `interaction_tolerance` (vectorized) | Maps to `SOCIAL_MINE_DIMENSIONS` — **social mine** sensitivity, not MBTI-style type. |
| `result_preview` | UX / sync status | Includes vector sync messaging. |

---

## Persistence files (outside Reflex state)

| File | Canonical buckets |
|------|-------------------|
| `runtime_state/user_profile.json` | `identity_signals`, partial `interaction_tolerance` |
| `runtime_state/fox_memory.json` | `social_drain_signals`, `guardian_notes`, history of patterns/warnings |

---

## Duplicated or overlapping meaning (watch list)

* **Activity:** profile numeric vs. `activity_analysis` string vs. demo peer `activity` — keep **one mental label**: “pressure / pace signal.”
* **Traits:** `shared_traits` (intersection) vs. user `interests` — dyadic vs. monadic; do not merge blindly in schema without provenance.

---

## Next steps (future sprints)

* Typed dataclass or Pydantic model mirroring `SIGNAL_PROFILE_SCHEMA.md` with explicit provenance fields.
* Gradual rename of `AppState` compatibility fields after regression plan.
