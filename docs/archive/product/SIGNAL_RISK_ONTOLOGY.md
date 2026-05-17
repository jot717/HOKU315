# SIGNAL RISK ONTOLOGY (v1)

**STATUS:** Canonical risk **type** vocabulary for rule engine + guardian copy.  
**Implementation:** Scores computed in [`product/signal/runtime/signal_inference_engine.py`](../../product/signal/runtime/signal_inference_engine.py) (repo root: `product/signal/runtime/signal_inference_engine.py`).

---

## RISK TYPES

### 1. `attention_drain_risk`

* **Meaning:** Attention is captured by fast feedback loops (DMs, mentions, reply anxiety); fatigue stacks before the user notices.
* **User experience:** “一直刷新／放不下手機”“一慢回就慌”类感受被点名，而非羞辱用户。
* **Future SNS mapping:** Reply velocity variance, mention bursts, session time spikes (opt-in).
* **Future graph signals:** High in-degree urgent edges, repeated @ from non-trusted clusters.
* **Guardian style:** Calm pacing, permission to mute, normalize slow replies.

### 2. `ghosting_sensitivity`

* **Meaning:** Slow replies / silence are read as high threat; emotional cost of ambiguity is high.
* **User experience:** 沈默、已讀不回被描述成「壓力源」，不說對方「壞」。
* **Future SNS mapping:** Read receipts off/on patterns, DM wait asymmetry.
* **Future graph signals:** One-way message ratios with specific alters.
* **Guardian style:** “沈默不一定是拒絕你這個人” — boundary + self-compassion.

### 3. `social_comparison_risk`

* **Meaning:** Life-stage / status comparison fields hurt more than average.
* **User experience:** 提醒離開比較場景，而非批評用户「嫉妒」。
* **Future SNS mapping:** Feed categories heavy on milestones; engagement with compare-bait.
* **Future graph signals:** Clusters discussing rank/salary/relationship milestones.
* **Guardian style:** Redirect to local pace and sleep, not debate.

### 4. `manipulation_sensitivity`

* **Meaning:** Ambiguous promises, mixed signals, plausible deniability cost extra cognitive load.
* **User experience:** 要求白話與界線，不渲染陰謀論。
* **Future SNS mapping:** Hedging language density in threads directed at user (policy-heavy).
* **Future graph signals:** Repeated push-pull dyads.
* **Guardian style:** “停一次、問清楚、可拒絕”。

### 5. `emotional_exhaustion_risk`

* **Meaning:** Self-reported stress + exposure mines suggest depleted bandwidth.
* **User experience:** 先止血（睡眠、留白），不做人生診斷。
* **Future SNS mapping:** Late-night usage, notification stacks.
* **Future graph signals:** Sustained high-urgency incoming edges.
* **Guardian style:** Recovery-first, reduce load.

### 6. `approval_dependency_risk`

* **Meaning:** External validation hooks are “loud”; backhanded praise / humblebrag contexts sting more.
* **User experience:** 辨識「明褒暗貶」場景，不標籤人格。
* **Future SNS mapping:** Compliment–criticism pairs in replies (future NLP, not v1).
* **Future graph signals:** Status games in replies to user’s posts.
* **Guardian style:** Name the pattern, not the person.

### 7. `passive_aggression_risk`

* **Meaning:** Cold treatment, sarcasm-as-joke, ambiguous silence drain more than open conflict.
* **User experience:** 描述「猜的成本」，不鼓勵撕破臉。
* **Future SNS mapping:** Sarcasm markers + thread temperature (future).
* **Future graph signals:** Indirect hostility cycles.
* **Guardian style:** Prefer clarity and exit over rumination.

### 8. `unsafe_circle_tolerance`

* **Meaning:** **Low** tolerance for harsh humor / debate spikes — high score = vulnerability in those venues (naming: score = exposure cost, not “high tolerance”).
* **User experience:** 建議避開高火藥味場子，不說用户「太脆弱」。
* **Future SNS mapping:** Quote-tweet fight depth, reply hostility.
* **Future graph signals:** Repeated conflict subgraph participation.
* **Guardian style:** Distance + curate inputs.

### 9. `overexposure_risk`

* **Meaning:** Groups, @ storms, interruption sensitivity overload cognitive bandwidth.
* **User experience:** 靜音、批次回、降低同步壓力。
* **Future SNS mapping:** Group ping rate, thread depth.
* **Future graph signals:** Large high-churn communities.
* **Guardian style:** Batch, mute, time-box.

### 10. `unstable_relationship_risk`

* **Meaning:** Boundary intrusion + cling / ambiguity mines suggest unpredictable closeness swings.
* **User experience:** 建議可預測的距離，不預言關係結果。
* **Future SNS mapping:** Volatile DM graphs (future).
* **Future graph signals:** On–off edge weight oscillation.
* **Guardian style:** Stabilize boundaries first.
