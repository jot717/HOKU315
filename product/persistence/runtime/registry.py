from __future__ import annotations

import os

from product.persistence.runtime.backend import LocalJsonBackend, PersistenceBackend
from product.persistence.runtime.cloud_backend import CloudPersistenceBackend
from product.persistence.runtime.dual_write_backend import DualWriteBackend
from product.persistence.runtime.sync_context import cloud_sync_enabled

_LOCAL = "local"
_DUAL = "dual"
_backend: PersistenceBackend | None = None


def get_backend() -> PersistenceBackend:
    """Return configured persistence backend."""
    global _backend
    if _backend is not None:
        return _backend
    mode = (os.environ.get("HOKU_PERSISTENCE_BACKEND") or _LOCAL).strip().lower()
    if mode == _LOCAL:
        _backend = LocalJsonBackend()
    elif mode == _DUAL:
        if not cloud_sync_enabled():
            _backend = LocalJsonBackend()
        else:
            _backend = DualWriteBackend(
                local=LocalJsonBackend(),
                cloud=CloudPersistenceBackend(),
            )
    elif mode == "cloud":
        raise ValueError(
            "HOKU_PERSISTENCE_BACKEND=cloud is not supported; use local or dual"
        )
    else:
        raise ValueError(
            f"unsupported HOKU_PERSISTENCE_BACKEND={mode!r}; "
            f"use {_LOCAL!r} or {_DUAL!r}"
        )
    return _backend


def reset_backend_for_tests() -> None:
    """Clear cached backend (tests / env changes only)."""
    global _backend
    _backend = None


def use_backend(backend: PersistenceBackend | None) -> None:
    """Inject backend for tests/UAT (does not replace imported get_backend refs)."""
    global _backend
    _backend = backend
