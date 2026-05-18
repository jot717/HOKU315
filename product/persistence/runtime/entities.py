from __future__ import annotations

from pathlib import Path

RUNTIME_ROOT = Path("runtime_state")

# Canonical entity keys (Phase 2-A foundation)
USER_PROFILE = "user_profile"
TARGET_PROFILE = "target_profile"
FOX_MEMORY = "fox_memory"
SESSION_HISTORY = "session_history"
LOCAL_SESSION = "local_session"

CLOUD_SYNCABLE_ENTITIES = frozenset(
    {
        USER_PROFILE,
        TARGET_PROFILE,
        FOX_MEMORY,
        SESSION_HISTORY,
    }
)

ENTITY_PATHS: dict[str, Path] = {
    USER_PROFILE: RUNTIME_ROOT / "user_profile.json",
    TARGET_PROFILE: RUNTIME_ROOT / "target_profile.json",
    FOX_MEMORY: RUNTIME_ROOT / "fox_memory.json",
    SESSION_HISTORY: RUNTIME_ROOT / "session_history.json",
    LOCAL_SESSION: RUNTIME_ROOT / "local_session.json",
}
