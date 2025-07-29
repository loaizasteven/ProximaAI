// import './index.css'
  import { createContext, useContext, useState, useEffect } from 'react'
  import { useLocation, useNavigate } from "react-router-dom";

  import { createClient } from '@supabase/supabase-js'
  import { Auth } from '@supabase/auth-ui-react'
  import { ThemeSupa } from '@supabase/auth-ui-shared'

  // Define Const
  const supabase = createClient(
    import.meta.env.VITE_SUPABASE_URL, 
    import.meta.env.VITE_SUPABASE_ANON_KEY
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
    
    
    useEffect(() => {
      if (session) {
        navigate(from, { replace: true });
      }
    }, [session, from, navigate]);
  
    if (!session) {
      return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
          <div style={{ width: '100%', maxWidth: '400px', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)', backgroundColor: 'white' }}>
            <Auth supabaseClient={supabase} appearance={{ theme: ThemeSupa }} />
          </div>
        </div>
      );
    }
    return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h2>You are already logged in!</h2>
      <p>Redirecting to your dashboard...</p>
    </div>
  );
  }