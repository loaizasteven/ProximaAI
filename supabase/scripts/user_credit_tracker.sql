CREATE TABLE user_credits (
  user_id uuid PRIMARY KEY REFERENCES auth.users(id),
  credits integer DEFAULT 10 -- starting balance
);