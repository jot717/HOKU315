# Deprecated entrypoint

Replay lives under the **AI layer**: [`ai/replay/replay_incident.py`](../ai/replay/replay_incident.py).

Preferred:

```powershell
python -m ai.replay.replay_incident --incident debug_evidence/YYYY-MM-DD-slug
```

The wrapper below forwards to that module when run from repo root.
