-- JOT717 / HOKU315：public.profiles RLS（新使用者可自行 INSERT／UPDATE 自己的列）
-- 修正 Task 6.5 聯調：42501（RLS 拒絕 INSERT profiles）導致後續 stories 23503（FK 無對應 profile）。
-- 前置：public.profiles 已存在，且主鍵欄位為 id uuid（與 auth.users.id 對齊）。
-- 於 Supabase SQL Editor 以具權限帳號執行。

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- authenticated：僅能讀寫列 id = auth.uid()
DROP POLICY IF EXISTS "profiles_select_own" ON public.profiles;
CREATE POLICY "profiles_select_own"
  ON public.profiles FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

DROP POLICY IF EXISTS "profiles_insert_own" ON public.profiles;
CREATE POLICY "profiles_insert_own"
  ON public.profiles FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "profiles_update_own" ON public.profiles;
CREATE POLICY "profiles_update_own"
  ON public.profiles FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- 確保 JWT 角色可對本身資料列下 DML（若專案尚未授予）
GRANT SELECT, INSERT, UPDATE ON public.profiles TO authenticated;
