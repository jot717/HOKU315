from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RUNTIME_ROOT = Path("runtime_state")
SYNC_STATUS_PATH = RUNTIME_ROOT / "sync_status.json"

_STATUSES = frozenset({"synced", "pending", "error", "local_only"})


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _default_doc() -> dict[str, Any]:
    return {"schema_version": 1, "entities": {}}


def load_sync_status() -> dict[str, Any]:
    if not SYNC_STATUS_PATH.exists():
        return _default_doc()
    try:
        with SYNC_STATUS_PATH.open(encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError):
        return _default_doc()
    if not isinstance(raw, dict):
        return _default_doc()
    entities = raw.get("entities")
    if not isinstance(entities, dict):
        raw["entities"] = {}
    return raw


def save_sync_status(doc: dict[str, Any]) -> None:
    SYNC_STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = SYNC_STATUS_PATH.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    tmp.replace(SYNC_STATUS_PATH)


def get_entity_status(entity: str) -> dict[str, Any]:
    doc = load_sync_status()
    row = doc.get("entities", {}).get(entity, {})
    if not isinstance(row, dict):
        row = {}
    return row


def mark_local_write(entity: str) -> None:
    doc = load_sync_status()
    entities = doc.setdefault("entities", {})
    row = dict(entities.get(entity, {}))
    row["local_updated_at"] = _utc_now_iso()
    entities[entity] = row
    save_sync_status(doc)


def mark_synced(entity: str, *, cloud_updated_at: str | None = None) -> None:
    doc = load_sync_status()
    entities = doc.setdefault("entities", {})
    row = dict(entities.get(entity, {}))
    row["status"] = "synced"
    row["last_error"] = ""
    if cloud_updated_at:
        row["cloud_updated_at"] = cloud_updated_at
    entities[entity] = row
    save_sync_status(doc)


def mark_pending(entity: str, error: str = "") -> None:
    doc = load_sync_status()
    entities = doc.setdefault("entities", {})
    row = dict(entities.get(entity, {}))
    row["status"] = "pending"
    if error:
        row["last_error"] = str(error)[:500]
    entities[entity] = row
    save_sync_status(doc)


def entity_local_timestamp(entity: str, path: Path) -> str:
    row = get_entity_status(entity)
    if row.get("local_updated_at"):
        return str(row["local_updated_at"])
    if path.exists():
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        return mtime.replace(microsecond=0).isoformat()
    return ""
