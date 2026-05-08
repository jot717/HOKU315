# MATCH STATE MODEL

## USER_STATE

- id
- profile
- match_status: idle | matching | matched | no_match

---

## MATCH_STATE

- user_id
- target_user_id
- score (0–100)
- status: pending | confirmed | rejected
- created_at
