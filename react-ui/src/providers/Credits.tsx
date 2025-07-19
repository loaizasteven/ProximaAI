import {useEffect, useState} from 'react'

interface CreditUpdateProps {
    authenticated: boolean;
    credit_usage: number;
    supabase: any;
    session: any;
}

export async function CreditUpdate({ 
  authenticated, 
  credit_usage, 
  supabase, 
  session 
}: CreditUpdateProps) {
  // Remove useSupabase() call - use the supabase parameter instead
  
  if (authenticated && session?.user?.id) {
    await supabase.rpc('spend_credits', {
      p_user_id: session.user.id,
      p_credits_to_spend: credit_usage ?? 1,
    });
  }
}
