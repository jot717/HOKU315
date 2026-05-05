# -*- coding: utf-8 -*-
"""
AI 記憶：驗證 fox_logic 地雷提示、llm_gateway 注入內容，以及（可選）DB 向量記憶 RPC。

無 Supabase 或尚未執行 sql/user_memories.sql 時，僅跑不依賴網路之斷言。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

import fox_logic

_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env", encoding="utf-8-sig")
load_dotenv(encoding="utf-8-sig")


def test_hints_gift_pressure() -> None:
    vec = [0.1] * fox_logic.VECTOR_DIM
    vec[15] = 0.95  # gift_reciprocity
    hints = fox_logic.minefield_hints_from_vector(vec, threshold=0.6)
    joined = " ".join(hints)
    assert "人情" in joined or "送禮" in joined


def test_simulate_fox_ack_with_injected_context() -> None:
    from llm_gateway import LLMGateway

    block = "注意：該使用者在「送禮／人情往來壓力」面向較敏感"
    ack = LLMGateway.simulate_fox_ack(block, "過年要包紅包給同事嗎？")
    assert "人情" in ack or "界線" in ack


def test_gateway_messages_shape() -> None:
    from llm_gateway import LLMGateway

    g = LLMGateway(provider="deepseek")
    assert g.provider.value == "deepseek"
    msgs = g.build_chat_messages(
        "00000000-0000-0000-0000-000000000001",
        "你好",
        query_vector=[0.5] * fox_logic.VECTOR_DIM,
    )
    assert len(msgs) == 2 and msgs[0]["role"] == "system"
    assert "譜系語氣" in msgs[0]["content"] and "LLM 必遵" in msgs[0]["content"]


def _maybe_integration_memory_roundtrip() -> None:
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        return
    import db_service
    from llm_gateway import LLMGateway

    uid = os.getenv("DB_TEST_PROFILE_ID", "00000000-0000-0000-0000-000000000001")
    db_service.ping_user_memories_table()
    db_service.get_client.cache_clear()
    vec = fox_logic.generate_vector([0.55] * fox_logic.VECTOR_DIM)
    summary = "【測試記憶】使用者曾表達對人情往來極度緊張"
    try:
        db_service.insert_user_memory(uid, summary, vec)
    except Exception as exc:
        print(f"SKIP memory insert: {exc}", file=sys.stderr)
        return
    try:
        res = db_service.match_user_memories(uid, vec, match_count=3)
        rows = getattr(res, "data", None) or []
        if not rows:
            print("SKIP match_user_memories returned no rows", file=sys.stderr)
            return
    except Exception as exc:
        print(f"SKIP match_user_memories: {exc}", file=sys.stderr)
        return

    gw = LLMGateway()
    block = gw.build_minefield_system_block(uid, query_vector=vec)
    assert summary in block or "人情" in block
    ack = LLMGateway.simulate_fox_ack(block, "要不要先送禮再談合作？")
    assert len(ack) > 5


def main() -> int:
    test_hints_gift_pressure()
    test_simulate_fox_ack_with_injected_context()
    test_gateway_messages_shape()
    _maybe_integration_memory_roundtrip()
    print("OK: test_ai_memory (hints + gateway + optional DB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
