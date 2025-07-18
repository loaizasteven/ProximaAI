# Supabase Backend

This directory contains the Supabase configuration and SQL scripts powering our backend infrastructure. Supabase provides our Postgres database, authentication, authorization, and secure data access for both the frontend application and backend LangGraph service.

## Features

- **User Authentication & Authorization:** Secure sign-up, email confirmation, and access control using Supabase Auth and Row Level Security (RLS).
- **User Credits System:** Automatically tracks and manages user credits upon email confirmation, with policies to ensure users can only view their own credits and cannot modify them directly.
- **Node Memory Cache:** Utilizes LangGraph's `Store` object with a Postgres backend for efficient caching and retrieval.

## Directory Structure

- `/scripts`: SQL files for creating tables, triggers, and functions.
  - `user_credit_tracker.sql`: Defines the `user_credits` table.
  - `user_credit_trigger_function.sql`: Trigger function to create user credits after email confirmation.
  - `set_trigger_on_auth.sql`: Sets up the trigger on the `auth.users` table.
- `/policies`: SQL files to enable Row Level Security and define access policies.
  - `security.sql`: Enables RLS and sets policies for the `user_credits` table.
- `/configuration`: Configuration files for Supabase, such as custom email templates.
  - `email_confirmation.html`: Custom HTML template for email confirmation.

## Setup

1. Run the SQL scripts in `/scripts` to set up tables, triggers, and functions.
2. Apply the policies in `/policies` to enforce security.
3. Configure Supabase project settings as needed (e.g., email templates in `/configuration`).

## Notes

- All database changes are managed via SQL files in this directory for transparency and reproducibility.
- See individual files for detailed comments and explanations.
