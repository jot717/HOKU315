# HOKU315

**AI social signal intelligence** - identify high-drain interaction patterns before they cost you energy.

Not a therapy app, dating score, or personality test.

---

## Product loop (Phase 1)

```
/profile -> /quiz -> /target -> /insight -> /match
```

Home `/` explains **guest** (analyze now) vs **account** (save trends). Login `/login` is optional.

---

## Core routes

| Route | Purpose |
|-------|---------|
| `/` | Entry |
| `/profile` | Signal profile |
| `/quiz` | Sensitivity questionnaire |
| `/target` | Observation target |
| `/insight` | Interaction pressure analysis |
| `/match` | Social energy compatibility |
| `/login` | Account utility |

---

## Guest vs account

| Mode | What you get |
|------|----------------|
| **Guest** | Local analysis on this device |
| **Account** | Cloud profile, match wall, history |

---

## Phase roadmap

| Phase | Scope |
|-------|--------|
| **1** | Local rule-based intelligence (now) |
| **2** | Persistence and memory |
| **3** | SNS import |
| **4** | Social graph |
| **5** | AI-scale inference |

Detail: [`docs/active/product/ROADMAP.md`](docs/active/product/ROADMAP.md)

---

## Repo structure

| Path | What |
|------|------|
| [`docs/active/product/`](docs/active/product/) | Product law (start at `PRODUCT_MASTER.md`) |
| [`docs/active/uat/`](docs/active/uat/) | Acceptance |
| [`docs/archive/`](docs/archive/) | History only |
| [`backlog/MASTER_BACKLOG.md`](backlog/MASTER_BACKLOG.md) | Sprint index |
| [`ops/governance/`](ops/governance/) | Engineering constitution |
| [`fox_quiz/`](fox_quiz/) | Reflex UI |
| [`product/`](product/) | Runtime engines |

**Doc navigation:** [`docs/README.md`](docs/README.md)

---

## Development law

1. [`docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md`](docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md)
2. [`ops/governance/DEVELOPMENT_CONSTITUTION.md`](ops/governance/DEVELOPMENT_CONSTITUTION.md)
3. [`ops/governance/REPO_ENTROPY_CHECKLIST.md`](ops/governance/REPO_ENTROPY_CHECKLIST.md)

---

## Quick start

```powershell
cd HOKU315
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ops/flow/check_all_flows.py
python -m pytest tests/regression/test_phase1h4_md_highway_v1.py -v --tb=short
python -m reflex run
```

Debug: [`ops/debug/DEBUG_GUIDE.md`](ops/debug/DEBUG_GUIDE.md) · Env: [`docs/active/env/STARTUP_GUIDE.md`](docs/active/env/STARTUP_GUIDE.md)
