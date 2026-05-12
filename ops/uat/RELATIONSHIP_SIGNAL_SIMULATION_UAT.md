# RELATIONSHIP SIGNAL SIMULATION — UAT (v1)

**TYPE:** Synthetic archetype + overlap simulation (no SNS / multi-user / vectors).  
**Refs:** [`ops/product/RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md`](../product/RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md)

---

## User understanding (pass)

* Users can paraphrase: the product is starting to talk about **how interactions behave**, not **who is bad** or **what personality type they are**.
* Guardian lines read as **socially relevant** (“有些人習慣…”, “這類互動會…”).

---

## Concrete vs abstract (pass)

* **Archetype strip** shows: name, **pressure** badge, **danger pattern** one-liner, **guardian hint**, **advice**, numeric **互動壓力指數**.
* Users report risks feel **tied to inputs** (activity + mine sensitivity + inference overlap), not random poetry.

---

## Therapy / diagnosis guardrails (fail if violated)

* Copy implies clinical diagnosis, moral judgment, or “你這個人很有問題” framing.

---

## Pass / fail checklist

| ID | Check | Pass |
|----|--------|------|
| R1 | 觀察室出現「北極狐正在警戒的互動類型」區塊 | 肉眼 |
| R2 | 主卡片副標改為互動耗損敘事（非「你很脆弱」） | 肉眼 |
| R3 | `generate_relationship_archetype` / `simulate_relationship_risk` 有固定輸出鍵 | pytest |
| R4 | 文檔三份存在 | pytest |
| R5 | 無新 `/onboarding` 路徑 | grep |
