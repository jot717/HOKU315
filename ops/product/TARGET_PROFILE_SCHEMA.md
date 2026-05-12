# TARGET PROFILE SCHEMA (v1)

Canonical JSON shape persisted at `runtime_state/target_profile.json` (SAFE MODE).

```json
{
  "target_name": "",
  "relationship_type": "",
  "observed_traits": [],
  "communication_style": [],
  "social_patterns": [],
  "pressure_signals": [],
  "instability_level": 0,
  "attention_demand": 0,
  "response_consistency": 0,
  "notes": ""
}
```

| Field | Meaning |
|--------|---------|
| `target_name` | Short label the user uses for this observation entity (not legal identity). |
| `relationship_type` | Coarse context (e.g. 同事、朋友、線上聯絡人) — informs tone, not judgment. |
| `observed_traits` | Observable behavior tags / phrases (user-authored). |
| `communication_style` | How contact tends to happen (e.g. 訊息忽冷忽熱、常語音長聊). |
| `social_patterns` | Recurring situational patterns (e.g. 低潮才出現、常改期). |
| `pressure_signals` | Pressure cues (e.g. 情緒勒索暗示、比較、模糊承諾). |
| `instability_level` | 0–10: rhythm unpredictability **as observed**. |
| `attention_demand` | 0–10: how often / how intensely the interaction seems to demand attention. |
| `response_consistency` | 0–10: higher = more predictable replies; lower = more erratic. |
| `notes` | Freeform user notes (optional). |

## Future SNS mapping

When connectors exist, optional fields may be populated from **consented** metadata (e.g. reply latency bands, thread depth) — still stored as **signals**, not identity verdicts.

## Future graph mapping

Targets may later link to graph nodes (handles, circles). v1 uses **no graph**: single local JSON record for the primary demo loop.

## Future AI signal extraction

Optional assist could propose tags for `pressure_signals` from user paste — **policy-gated**; v1 remains **manual + sliders** only.
