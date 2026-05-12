# SIGNAL PROFILE SCHEMA (v1 — CANONICAL)

**STATUS:** Canonical **target** schema for future persistence and APIs.  
**Today:** Existing JSON (`user_profile.json`, `fox_memory.json`) and in-memory state **partially** map into this shape; **no forced migration** in consolidation v1.

This schema is the **official** contract for “what a signal profile means” across profile, quiz, insight, memory, and future SNS.

---

## Canonical JSON shape

```json
{
  "identity_signals": {},
  "social_drain_signals": [],
  "pressure_triggers": [],
  "unsafe_interaction_patterns": [],
  "safe_patterns": [],
  "hater_sensitivity": [],
  "attention_drain_risk": [],
  "interaction_tolerance": [],
  "guardian_notes": [],
  "signal_history": []
}
```

---

## Field definitions

### `identity_signals` (object)

* **Purpose:** Stable self-described anchors (display name, interests tags, declared capacity) used to contextualize risk, not to “type” the user.
* **Future usage:** Merge `user_profile.json` fields (`name`, `interests`) and consent flags.
* **Future intelligence:** Feature attribution for “who this profile belongs to” in multi-device and SNS-linked graphs.
* **Future SNS mapping:** Link handles / accounts to the same identity bucket under strict consent.

### `social_drain_signals` (array)

* **Purpose:** Recurring **exhaustion** or **drain** tags derived from observation + memory (e.g. repeated high-pressure flags).
* **Future usage:** Feed guardian headlines and “why bullets” without long prose.
* **Future intelligence:** Time-decayed scoring, clustering with similar users (privacy-preserving).
* **Future SNS mapping:** Map thread tone / reply burden into drain tags.

### `pressure_triggers` (array)

* **Purpose:** Situations or topics that spike stress (from self-report + inferred patterns).
* **Future usage:** Pre-emptive warnings before user enters high-friction contexts.
* **Future intelligence:** Correlate with calendar / activity spikes when product allows.
* **Future SNS mapping:** Keyword and cadence triggers from opted-in feeds.

### `unsafe_interaction_patterns` (array)

* **Purpose:** Structural risk shapes (ghosting asymmetry, manipulation loop **labels** — conceptual; see [`HATER_SIGNAL_MODEL.md`](HATER_SIGNAL_MODEL.md)).
* **Future usage:** Danger alerts and safe-circle suggestions.
* **Future intelligence:** Graph + sequence models over interaction logs.
* **Future SNS mapping:** Cross-platform repetition of the same harm shape.

### `safe_patterns` (array)

* **Purpose:** Positive stabilizers (steady replies, mutual respect, recovery spacing).
* **Future usage:** Reinforce what to **keep**, not only what to avoid.
* **Future intelligence:** Contrast with drain signals for calibrated UX.
* **Future SNS mapping:** Identify supportive subgraphs.

### `hater_sensitivity` (array)

* **Purpose:** User-specific sensitivity to pile-ons, sarcasm, dogpiling — from quiz dimensions + history.
* **Future usage:** Tune alert thresholds per user.
* **Future intelligence:** Personalized hater-risk models.
* **Future SNS mapping:** Engagement velocity vs. negativity density.

### `attention_drain_risk` (array)

* **Purpose:** Risk of **attention farming** / doom-scrolling / bait engagement.
* **Future usage:** Pacing and “step back” interventions.
* **Future intelligence:** Session-level signals from app usage (where permitted).
* **Future SNS mapping:** Notification and mention burst patterns.

### `interaction_tolerance` (array)

* **Purpose:** Declared or inferred tolerance for conflict, ambiguity, rapid messaging (e.g. activity/stress slider + quiz dimensions).
* **Future usage:** Match guardian tone and density of warnings to user capacity.
* **Future intelligence:** Dynamic tolerance from observed opt-out behavior.
* **Future SNS mapping:** DM velocity vs. user response capacity.

### `guardian_notes` (array)

* **Purpose:** Short, user-visible **fox / guardian** lines tied to specific observations (append-only or capped list).
* **Future usage:** Replace scattered strings with a single append stream.
* **Future intelligence:** Summarization into weekly “signal digest.”
* **Future SNS mapping:** Map platform-specific events to one guardian note stream.

### `signal_history` (array)

* **Purpose:** Immutable or rolling log of **observation runs** (timestamps, risk level, key flags) — complements session history today.
* **Future usage:** Audit trail and regression of model behavior.
* **Future intelligence:** Train/evaluate without exposing raw messages prematurely.
* **Future SNS mapping:** Per-source ingestion history with revocation stamps.

---

## Current repo mapping (summary)

| Schema bucket | Today (approximate source) |
|---------------|----------------------------|
| `identity_signals` | `user_profile.json` (`name`, `interests`, `activity`) |
| `guardian_notes` / patterns | `fox_memory.json`, `AppState` guardian fields |
| `social_drain_signals` / `unsafe_interaction_patterns` | `signal_risk_flags`, recurring patterns from memory engine |
| `signal_history` | `session_history` append payloads (partial) |

Full mapping: [`SIGNAL_STATE_MAPPING.md`](SIGNAL_STATE_MAPPING.md).
