# TARGET SIGNAL PROFILE — UAT (v1)

**TYPE:** Local target JSON + insight integration (SAFE MODE).  
**Refs:** [`ops/product/TARGET_SIGNAL_CONSTITUTION.md`](../product/TARGET_SIGNAL_CONSTITUTION.md)

## User understanding (pass)

* Users can explain they are describing an **observation target**, not building a dating profile or diagnosing someone.
* Users know **who** the observation refers to (`target_name` + relationship type).

## Concrete interaction risk (pass)

* Insight shows a **target summary** when a name is saved.
* Guardian text reads as **「這個對象可能會…」** style bullets or equivalent when sliders/traits support it.

## Product loop clarity (pass)

* Home copy describes **social interaction protection** and the path includes **觀察對象** before or beside observation.

## Supportive fox tone (pass)

* No moral judgment of the target as a person; focus on **patterns** and **user safety**.

## Therapy / diagnosis guardrails (fail if violated)

* Language implies clinical diagnosis, "bad human" essentialism, or compatibility scoring as product core.

## Checklist

| ID | Check | Method |
|----|--------|--------|
| T1 | `/target` route exists | pytest / manual |
| T2 | Target file read/write | pytest |
| T3 | Insight compiles with simplified layout | pytest + `reflex compile` gate |
| T4 | Constitution + schema + flow docs on disk | pytest |
