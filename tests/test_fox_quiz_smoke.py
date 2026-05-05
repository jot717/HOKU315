# -*- coding: utf-8 -*-
"""
Reflex 狐狸測驗：匯入與 State 維度煙霧測試（不啟動 dev server）。
手動 UI 檢查清單：見 BACKLOG Task 2 備註。
"""
from __future__ import annotations

import fox_logic
from fox_quiz import chat_component
from fox_quiz import fox_quiz as fq


def main() -> int:
    assert fq.app is not None, "rx.App 應已建立"
    assert chat_component.chat_page is not None
    assert callable(getattr(chat_component.ChatState, "send_chat", None))

    scores_field = fq.QuizState.get_fields()["scores"]
    default_scores = scores_field.default_factory()
    assert len(default_scores) == fox_logic.VECTOR_DIM == 20
    vec = fox_logic.generate_vector(default_scores)
    assert len(vec) == 20 and all(isinstance(x, float) for x in vec)

    # 模擬 submit：全 0.25
    alt = [0.25] * 20
    v2 = fox_logic.generate_vector(alt)
    assert len(v2) == 20
    fox_msg = fox_logic.dominant_fox_message(v2)
    assert len(fox_msg) > 10 and "譜系" in fox_msg

    print("OK: fox_quiz app import + QuizState.scores dim + generate_vector pipeline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
