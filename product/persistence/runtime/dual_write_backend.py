from __future__ import annotations

from typing import Any

from product.persistence.runtime.backend import LocalJsonBackend, PersistenceBackend
from product.persistence.runtime.cloud_backend import (
    CloudPersistenceBackend,
    cloud_snapshot_updated_at,
)
from product.persistence.runtime.entities import LOCAL_SESSION
from product.persistence.runtime.sync_context import cloud_sync_active_for_entity
from product.persistence.runtime.sync_status import (
    entity_local_timestamp,
    mark_local_write,
    mark_pending,
    mark_synced,
)


class DualWriteBackend:
    """Local-first writes; cloud sync when enabled and authenticated."""

    def __init__(
        self,
        local: LocalJsonBackend | None = None,
        cloud: CloudPersistenceBackend | None = None,
    ) -> None:
        self._local = local or LocalJsonBackend()
        self._cloud = cloud or CloudPersistenceBackend()

    def path_for(self, entity: str):
        return self._local.path_for(entity)

    def read(self, entity: str) -> Any | None:
        if entity == LOCAL_SESSION or not cloud_sync_active_for_entity(entity):
            return self._local.read(entity)

        local_data = self._local.read(entity)
        snap = self._cloud.read_snapshot(entity)
        if snap is None:
            return local_data

        cloud_payload = snap.get("payload")
        cloud_ts = cloud_snapshot_updated_at(snap)
        local_ts = entity_local_timestamp(entity, self._local.path_for(entity))

        if cloud_ts and local_ts and cloud_ts > local_ts:
            if cloud_payload is not None:
                self._local.write(entity, cloud_payload)
                mark_synced(entity, cloud_updated_at=cloud_ts)
                return cloud_payload

        if cloud_ts and not local_ts and cloud_payload is not None:
            self._local.write(entity, cloud_payload)
            mark_synced(entity, cloud_updated_at=cloud_ts)
            return cloud_payload

        return local_data

    def write(self, entity: str, data: Any) -> None:
        self._local.write(entity, data)
        mark_local_write(entity)

        if entity == LOCAL_SESSION or not cloud_sync_active_for_entity(entity):
            return

        for attempt in range(3):
            try:
                self._cloud.write(entity, data)
                snap = self._cloud.read_snapshot(entity)
                mark_synced(entity, cloud_updated_at=cloud_snapshot_updated_at(snap))
                return
            except Exception as exc:
                if attempt == 2:
                    mark_pending(entity, str(exc))
                    return
        mark_pending(entity, "cloud write failed")
