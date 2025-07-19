CREATE OR REPLACE FUNCTION create_user_credits()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.email_confirmed_at IS NULL AND NEW.email_confirmed_at IS NOT NULL THEN
    BEGIN
      INSERT INTO public.user_credits (user_id, credits)
      VALUES (NEW.id, 10);
    EXCEPTION
      WHEN unique_violation THEN
        RAISE NOTICE 'user_credits row already exists for user_id: %', NEW.id;
        -- You can also insert into a log table here if you want
    END;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;