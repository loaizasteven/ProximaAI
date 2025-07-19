CREATE OR REPLACE FUNCTION spend_credits(
  p_user_id UUID, 
  p_credits_to_spend INTEGER
)
RETURNS INTEGER AS $$
DECLARE
  current_credits INTEGER;
  new_credits INTEGER;
BEGIN
  -- Get current credits with a lock to prevent concurrent modifications
  SELECT credits INTO current_credits
  FROM public.user_credits
  WHERE user_id = p_user_id
  FOR UPDATE;

  -- Check if user has enough credits
  IF current_credits < p_credits_to_spend THEN
    RAISE EXCEPTION 'Insufficient credits: % available, % requested', 
      current_credits, p_credits_to_spend;
  END IF;

  -- Calculate new credit balance
  new_credits := current_credits - p_credits_to_spend;

  -- Update credits
  UPDATE public.user_credits
  SET credits = new_credits
  WHERE user_id = p_user_id;

  RETURN new_credits;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

GRANT EXECUTE ON FUNCTION public.spend_credits(UUID, INTEGER) TO authenticated;