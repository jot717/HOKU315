from __future__ import annotations

import product.session.runtime.session_history as session_history


def test_session_history_append(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        session_history,
        "SESSION_HISTORY_PATH",
        tmp_path / "session_history.json",
    )

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
