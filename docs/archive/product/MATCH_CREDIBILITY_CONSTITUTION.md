# MATCH CREDIBILITY CONSTITUTION (Phase1-F)

> **Authority:** [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md)

## Purpose

Make `/match` and `/insight` feel **believable** through **social energy compatibility**—rhythm, reply pressure, pacing, and fatigue points—not template compatibility language.

## Product promise

We explain **how an interaction spends your social energy**, not whether you are a "good match" in a dating-app sense.

## Required match card elements

Each card (precomputed in Python) must include:

1. **Interaction rhythm** — archetype + rhythm detail  
2. **Reply pressure** — level + causal line  
3. **Emotional pacing** — tone/oscillation note  
4. **Social energy safety** — for this user + this peer shape  
5. **Likely exhaustion point** — where fatigue shows up  
6. **One scenario** — concrete micro-example  

## Forbidden

- "Great vibes", "high compatibility %" as the main story  
- Personality types (MBTI, attachment labels as identity)  
- Therapy/healing/diagnosis copy  
- Astrology or fate language  
- Dating-app scoring as hero metric  

## Fox (match + insight)

- Max **one** fox section per page  
- Observe patterns, explain pressure, suggest pacing  
- No excessive comfort, no mascot spam  

## Implementation

- Archetypes: `MATCH_ARCHETYPE_SYSTEM.md`  
- Energy model: `SOCIAL_ENERGY_MODEL.md`  
- Engine: `product/match/runtime/match_rhythm_engine.py`  
- UI: `fox_quiz/match_wall.py`, `fox_quiz/ui/insight_panel.py`  
