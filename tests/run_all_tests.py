# -*- coding: utf-8 -*-
"""
一鍵執行專案內所有 `tests.test_*` 模組之 `main()`。

- 無 Supabase／無 LLM API Key：純邏輯與 Reflex 煙霧測試仍應 exit 0；需雲端者自動 SKIP。
- 有 `.env`（SUPABASE_URL、SUPABASE_KEY 等）時：`test_db_connection`、`test_vector_persistence`、
  `test_ai_memory` 之整合段會盡力跑 E2E。
"""
from __future__ import annotations

import importlib
import sys
from typing import Callable

# 順序：無網路邏輯 → UI／Reflex → 可選 Supabase／記憶
_TEST_MODULES: tuple[str, ...] = (
    "tests.test_fox_logic",
    "tests.test_fox_quiz_smoke",
    "tests.test_ui_event",
    "tests.test_vector_persistence",
    "tests.test_ai_memory",
    "tests.test_story_auth",
    "tests.test_story_storage",
    "tests.test_auth_flow",
    "tests.test_hater_logic",
    "tests.test_db_connection",
)


def _run_one(name: str) -> int:
    mod = importlib.import_module(name)
    main: Callable[[], int] = getattr(mod, "main", None)
    if main is None:
        print(f"FAIL: {name} 缺少 main()", file=sys.stderr)
        return 1
    return int(main())


def main() -> int:
    print("=== JOT717 run_all_tests ===", flush=True)
    for name in _TEST_MODULES:
        print(f"--> {name}", flush=True)
        code = _run_one(name)
        if code != 0:
            print(f"FAIL: {name} exit {code}", file=sys.stderr)
            return code
    print("OK: all test modules passed (or SKIP where applicable)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
