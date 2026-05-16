# Future SNS / cloud session notes (implementers only)

This folder holds **non-user-facing** pointers for Phase 2+ implementation.

- **Session state:** `fox_quiz/session_state.py` persists auth-related fields for routes that still use cloud APIs (`/login`, `/story`, `/match` when backed by the existing stack). Field names may retain historical identifiers; **Phase1 UI must not** instruct users to paste secrets or debug tokens.
- **Backend:** `db_service.py` continues to use bearer/session semantics for PostgREST — this is **infrastructure**, not the Phase1 product narrative.
- **Phase 3:** SNS OAuth, external graph ingestion, and platform APIs belong in dedicated modules and gated onboarding — not in questionnaire or insight banners.

Do **not** link this directory from Phase1 product UX.
