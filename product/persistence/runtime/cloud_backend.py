from __future__ import annotations

from typing import Any

import db_service

from product.persistence.runtime.backend import PersistenceBackend
from product.persistence.runtime.sync_context import (
    cloud_sync_active_for_entity,
    get_access_token,
    resolve_sync_user_id,
)


class CloudPersistenceBackend:
    """Cloud entity snapshots via db_service only (no tokens in payload)."""

    def read(self, entity: str) -> Any | None:
        if not cloud_sync_active_for_entity(entity):
            return None
        user_id = resolve_sync_user_id()
        token = get_access_token()
        if not user_id or not token:
            return None
        snap = db_service.persistence_fetch_entity(
            user_id=user_id,
            entity_key=entity,
            access_token=token,
        )
        if snap is None:
            return None
        return snap.get("payload")

    def read_snapshot(self, entity: str) -> dict[str, Any] | None:
        """Full row with updated_at for conflict resolution."""
        if not cloud_sync_active_for_entity(entity):
            return None
        user_id = resolve_sync_user_id()
        token = get_access_token()
        if not user_id or not token:
            return None
        return db_service.persistence_fetch_entity(
            user_id=user_id,
            entity_key=entity,
            access_token=token,
        )

    def write(self, entity: str, data: Any) -> None:
        if not cloud_sync_active_for_entity(entity):
            return
        user_id = resolve_sync_user_id()
        token = get_access_token()
        if not user_id or not token:
            raise RuntimeError("cloud sync requires authenticated user")
        db_service.persistence_upsert_entity(
            user_id=user_id,
            entity_key=entity,
            payload=data,
            access_token=token,
        )


def cloud_snapshot_updated_at(snapshot: dict[str, Any] | None) -> str:
    if not snapshot:
        return ""
    return str(snapshot.get("updated_at") or "")
