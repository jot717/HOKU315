# SIGNAL SYSTEM CONSOLIDATION — UAT (v1)

**TYPE:** Architecture + copy consolidation (no new onboarding route)  
**PAIRING:** [`ops/product/SIGNAL_SYSTEM_CONSTITUTION.md`](../product/SIGNAL_SYSTEM_CONSTITUTION.md), [`ops/product/SIGNAL_FLOW_ARCHITECTURE.md`](../product/SIGNAL_FLOW_ARCHITECTURE.md)

---

## Expected understanding after onboarding (pass)

Users should be able to answer:

1. **What am I building?** — A **訊號檔案 / signal profile** (pressures, interests, pace), not a personality type card.
2. **What happens next?** — **觀察室** runs **guardian observation** on those signals (demo flow today).
3. **What is the optional depth?** — The **20 題滑桿** (`/quiz`) adds **社交地雷敏感度** dimensions to the same signal story.
4. **Where does memory go?** — **Signal memory** (local JSON) keeps short patterns so warnings are not one-shot.

---

## What users should believe the product does (pass)

* **Filters and interprets social-style signals** toward **protection** from draining or dangerous interaction patterns (aligned with [`CORE_PRODUCT_REALIGNMENT.md`](../product/CORE_PRODUCT_REALIGNMENT.md)).
* **Uses the fox** as the **guide** for those signals, not as the entire “engine” story.

---

## What users should NOT think the product is (fail if implied)

* A **standalone AI therapy** or healing app.
* A **personality test** or typology product (quiz is **mine sensitivity**, not “你的型”).
* A **dating / compatibility** app (deprecated framing).
* A **second onboarding product** if they already completed `/profile` — no duplicate “tell us about yourself” journey elsewhere.

---

## Pass / fail criteria

| ID | Criterion | Pass |
|----|-----------|------|
| U1 | Home shows ordered steps: profile → fox learns patterns → observation → future social layer | User can recite order after reading home |
| U2 | `/profile` copy never calls the file a “性格” or “心理” profile | Spot check Traditional Chinese strings |
| U3 | No new `/onboarding*` route appears in `fox_quiz.py` | Repo grep |
| U4 | `/insight` and `/profile` still load (smoke) | Manual or compile gate |
| U5 | Constitution + schema + flow + audit + state mapping docs exist in `ops/product/` | CI doc regression test |

---

## Evidence checklist

* Screenshot or note: home “路徑” block visible above primary CTAs.
* Screenshot: profile success still offers **進入觀察室**.
