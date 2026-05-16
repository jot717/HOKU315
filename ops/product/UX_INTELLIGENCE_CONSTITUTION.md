# UX INTELLIGENCE CONSTITUTION (Phase1-D)

## Purpose

Add a **human-like social interaction reasoning layer** that explains **how social pressure drains the user**—without LLM, therapy framing, or personality diagnosis.

## What this layer is

- Rule-based mapping from profile, quiz vector, inference, target, and relationship simulation.
- Short, **causal**, **observational** copy for `/insight` and `/match`.
- One **fox observer** block maximum on insight (quiet interpreter, not mascot).

## What this layer is not

- Not LLM generation.
- Not therapy, healing, or life coaching.
- Not personality typing ("you are an X person").
- Not medical or psychiatric diagnosis.
- Not certainty theater ("this will definitely…").

## Fox role

| Fox is | Fox is not |
|--------|------------|
| Observer of interaction shape | Therapist |
| Quiet signal guide | Emotional healer |
| Names pressure patterns | Anime mascot monologue |

## Output contract

Functions in `ux_intelligence_engine.py` return **plain strings** suitable for Reflex state—precomputed in Python, not compared inside `rx.foreach`.

## Phase boundary

Phase1 face uses this engine for **local signal + questionnaire + target** reasoning only. SNS/OAuth/API copy must not re-enter primary UI (see `PHASE_BOUNDARY_SYSTEM.md`).
