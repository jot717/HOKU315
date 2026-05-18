from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

import db_service

_TOKEN_PROVIDER: Callable[[], str | None] | None = None


def set_access_token_provider(provider: Callable[[], str | None] | None) -> None:
    """Register app-layer token source (e.g. SessionState). Tests may omit."""
    global _TOKEN_PROVIDER
    _TOKEN_PROVIDER = provider


def get_access_token() -> str | None:
    if _TOKEN_PROVIDER is not None:
        token = _TOKEN_PROVIDER()
        if token and str(token).strip():
            return str(token).strip()
    env = (os.environ.get("HOKU_ACCESS_TOKEN") or "").strip()
    return env or None


def cloud_sync_enabled() -> bool:
    return (os.environ.get("HOKU_CLOUD_SYNC_ENABLED") or "").strip().lower() in (
        "1",
        "true",
        "yes",
    )


def resolve_sync_user_id() -> str | None:
    return db_service.resolve_user_id(access_token=get_access_token())


def cloud_sync_active_for_entity(entity: str) -> bool:
    from product.persistence.runtime.entities import CLOUD_SYNCABLE_ENTITIES, LOCAL_SESSION

    if entity == LOCAL_SESSION:
        return False
    if entity not in CLOUD_SYNCABLE_ENTITIES:
        return False
    if not cloud_sync_enabled():
        return False
    return resolve_sync_user_id() is not None
