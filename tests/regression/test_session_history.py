from __future__ import annotations

import product.session.runtime.session_history as session_history
from product.persistence.runtime import registry
from product.persistence.runtime.backend import LocalJsonBackend
from product.persistence.runtime.entities import SESSION_HISTORY


def test_session_history_append(tmp_path) -> None:
    registry.use_backend(LocalJsonBackend({SESSION_HISTORY: tmp_path / "session_history.json"}))

    session_history.append_history(
        {
            "final_insight": "test",
        }
    )

    history = session_history.load_history()

    assert len(history) >= 1
    row = history[0]
    assert set(row.keys()) >= {"final_insight", "compatibility_title", "energy_summary"}
    assert isinstance(row["final_insight"], str)
