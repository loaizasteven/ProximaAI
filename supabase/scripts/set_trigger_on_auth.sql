-- More secure trigger with explicit checks
CREATE OR REPLACE TRIGGER trigger_create_user_credits
AFTER UPDATE OF email_confirmed_at ON auth.users
FOR EACH ROW
WHEN (
  NEW.email_confirmed_at IS NOT NULL AND 
  OLD.email_confirmed_at IS NULL AND 
  -- Additional security: Only allow for new users
  NEW.created_at > NOW() - INTERVAL '5 minutes'
)
EXECUTE FUNCTION create_user_credits();
