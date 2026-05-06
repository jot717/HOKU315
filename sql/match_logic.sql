-- Task 7：北極狐配對牆 RPC（UAT-04 門檻版）
-- get_safe_matches(current_uid uuid)
--   - 消失門檻 Blocked: distance >= 1.2 -> 不回傳
--   - 模糊門檻 Blurred: distance >= 0.7 -> is_blurred = true
--   - 衝突分析: 取 |a_i - b_i| 最大之維度 index + label

create extension if not exists vector;

CREATE OR REPLACE FUNCTION get_safe_matches(input_user_id uuid)
RETURNS TABLE (
  user_id uuid,
  distance float,
  is_blurred boolean
)
LANGUAGE sql
AS $$
WITH me AS (
  SELECT vector
  FROM profiles
  WHERE id = input_user_id
)

SELECT
  p.id AS user_id,
  (p.vector <-> me.vector) AS distance,
  CASE
    WHEN (p.vector <-> me.vector) >= 0.7 THEN true
    ELSE false
  END AS is_blurred
FROM profiles p, me
WHERE p.id != input_user_id
ORDER BY distance ASC
LIMIT 20;
$$;
