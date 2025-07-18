// import './index.css'
  import { createContext, useContext, useState, useEffect } from 'react'
  import { useLocation, useNavigate } from "react-router-dom";

  import { createClient } from '@supabase/supabase-js'
  import { Auth } from '@supabase/auth-ui-react'
  import { ThemeSupa } from '@supabase/auth-ui-shared'

  // Define Const
  const supabase = createClient(
    import.meta.env.VITE_SUPABASE_URL, 
    import.meta.env.VITE_SUPABASE_KEY
  )
  export const AuthContext = createContext(null)
  export const SupabaseContext = createContext(supabase);

 function Authentication({ children }) {
    const [session, setSession] = useState(null)

    useEffect(() => {
      supabase.auth.getSession().then(({ data: { session } }) => {setSession(session)})
      const {data: { subscription },} = supabase.auth.onAuthStateChange((_event, session) => {setSession(session)})
      return () => subscription.unsubscribe()
    }, [])  
    return (
      <SupabaseContext.Provider value={supabase}>
        <AuthContext.Provider value={session}>
          {children}
        </AuthContext.Provider>
      </SupabaseContext.Provider>
    )
  }

  // Export functions
  export default Authentication

  export function useAuth() {
    return useContext(AuthContext)
  };
  export function useSupabase() {
    return useContext(SupabaseContext);
  }

  export function LoginForm() {
    const session = useAuth();
    const location = useLocation();
    const navigate = useNavigate();
    const from = location.state?.from?.pathname || "/products";
    async function signOut() {
      // sign out from the current session only
      const { error } = await supabase.auth.signOut({ scope: 'local' })
    }
    
    useEffect(() => {
      if (session) {
        navigate(from, { replace: true });
      }
    }, [session, from, navigate]);
  
    if (!session) {
      return <Auth supabaseClient={supabase} appearance={{ theme: ThemeSupa }} />;
    }
    return (
      <div>
        Logged in!
        <button onClick={signOut}>log out</button>
      </div>
    );
  }