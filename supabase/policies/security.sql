-- Enable Row Level Security
ALTER TABLE public.user_credits ENABLE ROW LEVEL SECURITY;

-- Policy to restrict credit modifications
CREATE POLICY "Users can only view their own credits" 
ON public.user_credits 
FOR ALL 
TO anon, authenticated 
USING (user_id = auth.uid());

-- Policy to prevent direct credit updates
CREATE POLICY "Prevent direct credit modifications" 
ON public.user_credits 
FOR UPDATE 
TO anon, authenticated 
WITH CHECK (false);