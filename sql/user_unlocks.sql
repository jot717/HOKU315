-- Task 9：使用者對某 profile（target）的解鎖紀錄（最小表）
-- 於 Supabase SQL Editor 執行。

CREATE TABLE IF NOT EXISTS public.user_unlocks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES public.profiles (id) ON DELETE CASCADE,
  target_id uuid NOT NULL REFERENCES public.profiles (id) ON DELETE CASCADE,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (user_id, target_id)
);

CREATE INDEX IF NOT EXISTS user_unlocks_user_id_idx ON public.user_unlocks (user_id);

ALTER TABLE public.user_unlocks ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "user_unlocks_select_own" ON public.user_unlocks;
CREATE POLICY "user_unlocks_select_own"
  ON public.user_unlocks FOR SELECT TO authenticated
  USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "user_unlocks_insert_own" ON public.user_unlocks;
CREATE POLICY "user_unlocks_insert_own"
  ON public.user_unlocks FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id);

GRANT SELECT, INSERT ON public.user_unlocks TO authenticated;
