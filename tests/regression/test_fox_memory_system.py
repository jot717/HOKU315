from __future__ import annotations

import product.memory.runtime.fox_memory_store as fox_memory_store
from fox_quiz.ui.components.fox_memory_card import fox_memory_card
from fox_quiz.ui.insight_panel import insight_panel
from product.memory.runtime.fox_memory_engine import remember_insight


def test_fox_memory_engine_returns_dict(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(fox_memory_store, "MEMORY_PATH", tmp_path / "fox_memory.json")
    out = remember_insight({"shared_traits": ["quiet"]}, 72.0)
    assert isinstance(out, dict)
    assert "guardian_memory_note" in out
    assert "recurring_pattern" in out
    assert len(out["guardian_memory_note"]) > 0


def test_fox_memory_insight_panel_and_card_compile() -> None:
    assert insight_panel() is not None
    assert fox_memory_card("", "") is not None
    assert fox_memory_card("我記得你最近常避開高壓訊號。", "最近讓你疲憊的互動似乎變少了。") is not None
