from __future__ import annotations

import os
from product.persistence.runtime.backend import LocalJsonBackend, PersistenceBackend

_LOCAL = "local"
_backend: PersistenceBackend | None = None


def get_backend() -> PersistenceBackend:
    """Return configured persistence backend. Phase 2-A: local JSON only."""
    global _backend
    if _backend is not None:
        return _backend
    mode = (os.environ.get("HOKU_PERSISTENCE_BACKEND") or _LOCAL).strip().lower()
    if mode != _LOCAL:
        raise ValueError(
            f"unsupported HOKU_PERSISTENCE_BACKEND={mode!r}; "
            f"Phase 2-A supports {_LOCAL!r} only"
        )
    _backend = LocalJsonBackend()
    return _backend


def reset_backend_for_tests() -> None:
    """Clear cached backend (tests / env changes only)."""
    global _backend
    _backend = None
