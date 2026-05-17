# INTERACTION SIGNAL ONTOLOGY (v1)

**STATUS:** Canonical **interaction-level** signal vocabulary (not user-worth metrics).  
Used by synthetic archetypes and overlap rules in [`relationship_simulation_engine.py`](../../product/signal/runtime/relationship_simulation_engine.py).

---

## SIGNAL TYPES

### delayed reassurance

* **Meaning:** Comfort or clarity arrives late or never after a spike of anxiety.
* **Future SNS mapping:** DM read receipts + long gaps before substantive replies.
* **Future graph mapping:** Repeated long-latency edges from same alter after distress cues.
* **Guardian interpretation:** Normalize slow replies without self-blame; name the **asymmetry** not the person.
* **Exhaustion impact:** Keeps nervous system in “pending” state.

### emotional ambiguity

* **Meaning:** Mixed signals — warmth and distance alternate without clear boundaries.
* **Future SNS mapping:** Ambiguous threads, story replies that contradict DMs (future).
* **Future graph mapping:** Oscillating sentiment arcs between two nodes.
* **Guardian interpretation:** Ask for plain language commitments; pause before over-investing.
* **Exhaustion impact:** High cognitive load (“reading the air”).

### attention extraction

* **Meaning:** Interactions that harvest focus and care without proportional return.
* **Future SNS mapping:** Bait posts, vague “@someone” drama, notification pile-ons.
* **Future graph mapping:** High outbound support edges, low reciprocity.
* **Guardian interpretation:** Batch replies, mute bursts, protect sleep.
* **Exhaustion impact:** Attention bankruptcy.

### pressure escalation

* **Meaning:** Demands or emotional temperature ratchet up faster than recovery windows allow.
* **Future SNS mapping:** Escalating thread depth, quote-fights.
* **Future graph mapping:** Rising conflict weight on edges week-over-week.
* **Guardian interpretation:** Stepwise boundaries; exit ramps before peak.
* **Exhaustion impact:** Adrenaline debt.

### unstable affection

* **Meaning:** Closeness swings — hot then cold — destabilizing prediction.
* **Future SNS mapping:** Follow/unfollow churn, blocking cycles (future, policy-bound).
* **Future graph:** On–off edge weights.
* **Guardian interpretation:** Prefer predictable distance over chaotic intimacy.
* **Exhaustion impact:** Attachment system overload.

### social comparison pressure

* **Meaning:** Milestone / status framing that shrinks self-worth.
* **Future SNS mapping:** Feed segments dominated by progress flex.
* **Future graph:** Peers in “showcase” subgraphs.
* **Guardian interpretation:** Curate inputs; return to personal pace.
* **Exhaustion impact:** Shame-fatigue loop.

### passive hostility

* **Meaning:** Hostility delivered as jokes, silence, or plausible deniability.
* **Future SNS mapping:** Sarcasm markers + dogpiling tone (future NLP).
* **Future graph:** Indirect attack paths.
* **Guardian interpretation:** Prefer clarity over mind-reading.
* **Exhaustion impact:** Rumination.

### emotional unpredictability

* **Meaning:** Hard to forecast reactions; user must stay hypervigilant.
* **Future SNS mapping:** Volatile reply sentiment sequences.
* **Future graph:** High variance interaction outcomes with same alter.
* **Guardian interpretation:** Reduce synchronous exposure; schedule boundaries.
* **Exhaustion impact:** Hypervigilance tax.

### guilt-driven interaction

* **Meaning:** Requests framed so “no” feels cruel or disloyal.
* **Future SNS mapping:** Public obligation posts (future).
* **Future graph:** Guilt-heavy reciprocity asymmetry.
* **Guardian interpretation:** Permission to refuse; separate care from compliance.
* **Exhaustion impact:** Moral fatigue.

### validation farming

* **Meaning:** Fishing for reassurance / praise while avoiding commitment or reciprocity.
* **Future SNS mapping:** Performative vulnerability loops (future detection).
* **Future graph:** One-way affirmation harvesting.
* **Guardian interpretation:** Match words to actions over time.
* **Exhaustion impact:** Emotional labor skew.

---

## NOTE

v1 uses these tokens inside **archetype** `interaction_signals[]` lists; SNS/graph columns are **forward-looking** only.
