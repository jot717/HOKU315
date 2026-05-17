# DRIFT REPORT (scan — no auto-removal)

Automated / manual scan for wording that may conflict with **FOX GUARDIAN SYSTEM** positioning (`PRODUCT_CONSTITUTION.md`): not a dating app; signal / protection first; calm, low-pressure UX.

Scan terms: `compatibility`, `dating`, `emotional energy`, `shared energy`, romantic-adjacent wording.

---

## Summary

| Term | Approx. hits | Notes |
|------|----------------|-------|
| compatibility | Many (code + docs) | Often dating-app adjacent framing |
| dating | 0 literal in `.md` / `.py` | No English “dating” string in scanned globs |
| emotional energy / 互動能量 | Few | Pair-energy / chemistry tone |
| shared energy | 0 exact phrase | Overlap via `energy_summary` + English copy |
| romantic / 曖昧 / 戀愛 | Very few | See rows below |

---

## Findings (file · wording · drift rationale)

### Compatibility (dating-adjacent framing)

| File | Wording | Why it drifts |
|------|---------|----------------|
| `product/insight/experience/insight_formatter.py` | `Exceptional Compatibility`, `Strong Potential`, `Unexpected Dynamic` | Reads like relationship / match-product scoring, not guardian / safety framing. |
| `product/insight/experience/insight_formatter.py` | `compatibility_title` keys and English couple copy (`amplify each other's energy`, `naturally balanced`) | Pair-romance narrative; weak link to protection / filtering / danger signals. |
| `fox_quiz/ui/components/hero_insight.py` | `配對共鳴指數` | “配對 + 共鳴” centers pairing chemistry vs. fox-world safety. |
| `fox_quiz/ui/components/compatibility_meter.py` | `compatibility_meter` (symbol name) | Technical; still brands primary metric as “compatibility.” |
| `fox_quiz/state/app_state.py` | `compatibility_title`, `match_score_heading` | State names surface dating-style compatibility as hero concept. |
| `product/insight/README.md` | `Generate compatibility insight from match data.` | Product doc anchors insight on compatibility, not guardian mission. |
| `product/INTERFACE.md` | `generate user compatibility results` | Interface language locks “compatibility” as core output. |
| `product/insight/__init__.py` | `compatibility insight from match data` | Same as README — narrows product story. |
| `BACKLOG.md` | `Dynamic compatibility insight generation.` | Governance doc repeats dating-adjacent vocabulary. |
| `ops/uat/README.md` | `compatibility meter shown` | UAT checklist reinforces meter-as-product centerpiece. |
| `backlog/BACKLOG_INSIGHT_ENGINE_v1.md` | `compatibility insight`, `compatibility reasoning` | Historical sprint language. |
| `backlog/SPRINT_INSIGHT_ENGINE_v1.md` | `compatibility summary generation` | Same. |
| `backlog/SPRINT_INSIGHT_EXPERIENCE_v1.md` | `compatibility display` | Same. |
| `backlog/SPRINT_UNLOCK_FLOW_v1.md` | `compatibility insight generator` | Same. |
| `backlog/SPRINT_PHASE1_FINALIZATION.md` | `compatibility meter` | Same. |
| `product/insight/state_model.md` | `compatibility_score` | Schema language. |
| `product/unlock/state_model.md` | `compatibility_score` | Same. |
| `product/unlock/product_flow.md` | `[Generate Compatibility Insight]` | Flow label reads as dating-product feature. |
| `tests/regression/test_insight_flow.py` | asserts `compatibility_score` | Test contract (not wrong); vocabulary is drift-prone. |
| `tests/regression/test_unlock_flow.py` | asserts `compatibility_score` | Same. |
| `tests/regression/test_flow_integration.py` | asserts `compatibility_score` | Same. |
| `tests/regression/test_insight_experience.py` | asserts `compatibility_title` | Same. |

### Emotional energy / “energy” pair narrative

| File | Wording | Why it drifts |
|------|---------|----------------|
| `fox_quiz/ui/insight_panel.py` | `AI 正在分析你們的互動能量...` | “You two” interaction-energy trope; closer to chemistry / dating-app loading copy than guardian / signal filter. |
| `product/insight/experience/insight_formatter.py` | `You naturally amplify each other's energy.` | Explicit mutual romantic-energy idiom. |
| `product/insight/experience/insight_formatter.py` | `energy_summary` field + tension / overlap lines | Frames insight as relational chemistry vs. safety / boundaries. |

### Shared energy (conceptual — no exact heading string in repo)

| File | Wording | Why it drifts |
|------|---------|----------------|
| `fox_quiz/state/app_state.py` | `energy_summary` (persisted with session) | Naming + downstream UI tie insight to “energy” dyad framing. |
| `tests/regression/test_insight_experience.py` | asserts `energy_summary` | Locks the above contract. |

### Dating / 配對 / wall language (no English “dating”, but product-adjacent)

| File | Wording | Why it drifts |
|------|---------|----------------|
| `fox_quiz/fox_quiz.py` | page title `配對牆` | “Wall of matches” pattern mirrors dating-app discovery surfaces. |
| `fox_quiz/match_wall.py` | `北極狐配對牆`, `刷新配對牆` | Same — emphasis on pairing volume / refresh loop. |
| `fox_quiz/nav_bar.py` | `配對牆` | Nav label reinforces dating-wall mental model. |
| `fox_quiz/login_page.py` | `← 配對牆` | Same. |
| `fox_quiz/ui/pages/home_page.py` | `開始 AI 配對解析` | CTA centers “配對” (pairing) not guardian / safety. |
| `fox_quiz/ui/insight_panel.py` | `開始你的 AI 配對解析`, onboarding `個人資料 → 配對解析 → 檢視洞察` | Linear “pairing first” journey vs. constitution’s “matching is one part of signal system.” |
| `fox_quiz/ui/app_page.py` | `AI 情緒配對解析` | Same. |
| `SPRINT_PLAN.md` | `穩定核心配對流程` | Planning language elevates 配對 as core vs. signal system. |
| `backlog/BACKLOG_MATCH_FLOW_v1.md` | `用戶配對系統 MVP` | Explicitly match-first MVP framing. |

### Romantic-adjacent / ambiguity wording

| File | Wording | Why it drifts |
|------|---------|----------------|
| `fox_logic.py` | dimension label `訊號模糊（曖昧不清）` | “曖昧” can read as romance-adjacent; here it is a **social minefield** dimension — may still scan badly in isolation. Review copy in guardian context. |

---

## Grep notes

* **Literal `dating`**: no matches in `*.md` / `*.py` at scan time (does not mean UX is non-dating; Chinese `配對` carries much of the risk).
* **`shared energy`**: no exact English heading string found; overlap is via `energy_summary` + formatter English.
* **Auto-delete**: intentionally **not** performed per cleanup mandate; use this file to prioritize copy / API renames in a future alignment sprint.
