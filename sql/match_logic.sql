-- Task 7：北極狐配對牆 RPC（UAT-04 門檻版）
-- get_safe_matches(query_vector vector)
--   - 模糊門檻 Blurred: distance >= 0.7 -> is_blurred = true

create extension if not exists vector;

CREATE OR REPLACE FUNCTION get_safe_matches(query_vector vector)
RETURNS TABLE (
  user_id uuid,
  distance float,
  is_blurred boolean
)
LANGUAGE sql
AS $$
SELECT
  p.id AS user_id,
  (p.vector <-> query_vector) AS distance,
  CASE
    WHEN (p.vector <-> query_vector) >= 0.7 THEN true
    ELSE false
  END AS is_blurred
FROM profiles p
ORDER BY distance ASC
LIMIT 20;
$$;
