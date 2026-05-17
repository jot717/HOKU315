# SIGNAL INPUT AUDIT (v1)

**STATUS:** Consolidation audit — **no removals** in this sprint  
**Goal:** List what already collects or represents **signals**, where overlap and drift are, and what becomes **canonical**.

---

## What already exists

| Surface / module | Inputs | Output / persistence |
|-------------------|--------|----------------------|
| **`/profile`** (`profile_page.py`, `ProfileState`) | Name, interests (comma text), activity/stress 1–10 | `runtime_state/user_profile.json` (`name`, `interests`, `activity`) |
| **`/quiz`** (`fox_quiz.py` `QuizState`) | 20 sliders 0–1 per `SOCIAL_MINE_DIMENSIONS` | In-memory scores → `generate_vector` → optional Supabase `upsert_user_vector` when logged in |
| **`/insight`** (`insight_panel.py`, `AppState`) | Loads profile + runs `execute_bound_flow` demo | `insight_state`, `flow_result`, guardian risk, fox memory updates |
| **Signal guard** (`signal_guard_engine.py`) | `insight_state` + match score + `fox_memory.json` | `risk_level`, `risk_flags`, `guardian_warning`, `guardian_action` |
| **Fox memory** (`fox_memory_store.py`, `fox_memory_engine.py`) | Recent patterns/warnings from observations | `runtime_state/fox_memory.json` |
| **Session history** (`session_history.py`) | Appends titles/summaries after demo match | History list in `AppState` |
| **Insight engine** (`insight_engine.py`) | Interests overlap, activity diff, match score | `ai_summary`, `shared_traits`, `activity_analysis` (English strings today) |

---

## Overlaps

* **Stress / capacity:** Profile `activity` (1–10) **and** insight `activity_analysis` / flow activity diff — same *theme*, different layers (self-report vs. computed narrative).
* **“Energy” vs signal risk:** Memory still has `last_seen_energy` key in store default; UI leans on **guardian / risk** language — naming drift only.
* **Interests:** Profile `interests` **and** insight `shared_traits` (intersection with demo peer) — both “social signal” but **different semantics** (self vs. dyadic demo).

---

## What drifted

* **Quiz** module title “狐狸性向測驗” reads **personality-adjacent** though dimensions are **social mine** sensitivity — UX story should stay **signal / mine** not typing.
* **Insight engine** copy is **English** and **compatibility-flavored** internally; guardian UI partially hides this but schema still exposes `compatibility_title`-style state names in `AppState` (identifier drift vs. “signal product”).
* **Onboarding narrative** split across home, profile callouts, and insight strip — same journey, **three voices** until consolidation copy pass.

---

## Canonical (locked for new work)

| Concern | Canonical surface / artifact |
|---------|------------------------------|
| Portable user signal file | **`/profile`** + `user_profile.json` |
| Deep mine sensitivity vector | **`/quiz`** sliders + vector pipeline |
| Observation + guardian output | **`/insight`** + `AppState` + signal guard |
| Longitudinal tone | **`fox_memory.json`** + session history |

---

## Deprecate later (not in v1 code removal)

* Renaming `AppState.compatibility_*` fields to `signal_match_*` or similar (contract / regression scope).
* Replacing English `insight_engine` strings with locale-neutral or guardian-scripted summaries.
* Retiring `last_seen_energy` if unused in UI.

---

## References

[`SIGNAL_SYSTEM_CONSTITUTION.md`](SIGNAL_SYSTEM_CONSTITUTION.md) · [`SIGNAL_PROFILE_SCHEMA.md`](SIGNAL_PROFILE_SCHEMA.md) · [`SIGNAL_STATE_MAPPING.md`](SIGNAL_STATE_MAPPING.md)
