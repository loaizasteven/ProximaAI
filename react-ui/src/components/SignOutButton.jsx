// src/components/SignOutButton.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useSupabase } from '../auth/Authentication'; // Adjust path based on your project structure

/**
 * SignOutButton Component
 *
 * This component provides a button that, when clicked, signs the user out
 * of their current Supabase session. Upon successful sign-out, it redirects
 * the user to the login page.
 */
const SignOutButton = () => {
  const supabase = useSupabase(); // Access the Supabase client from context
  const navigate = useNavigate(); // Hook for programmatic navigation

  /**
   * Handles the sign-out process.
   * Calls Supabase's signOut method and manages redirection and error handling.
   */
  const handleSignOut = async () => {
    try {
      // Call Supabase's signOut method.
      // The `scope: 'local'` ensures only the current browser session is signed out.
      const { error } = await supabase.auth.signOut({ scope: 'local' });

      if (error) {
        // Log any errors that occur during sign-out
        console.error('Error signing out:', error.message);
        // In a real application, you might display a user-friendly error message here
      } else {
        // Log successful sign-out
        console.log('User signed out successfully');
        // Supabase automatically clears session data from browser storage.
        // The `onAuthStateChange` listener in Authentication.jsx will detect the session change
        // and set the session state to null, which will then trigger the RequireAuth
        // component to redirect to the login page.
        // Explicitly navigating here provides immediate visual feedback to the user.
        navigate('/login'); // Redirect to the login page after successful sign out
      }
    } catch (error) {
      // Catch any unexpected errors during the sign-out process
      console.error('Unexpected error during sign out:', error.message);
      // In a real application, you might display a general error message
    }
  };

  return (
    <button
      onClick={handleSignOut}
      style={{
        padding: '10px 20px',
        backgroundColor: '#dc3545', // Red color for danger/sign-out actions
        color: 'white',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer',
        fontSize: '16px',
        fontWeight: 'bold',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        transition: 'background-color 0.3s ease, transform 0.2s ease',
        // Hover effects
        ':hover': {
          backgroundColor: '#c82333',
        },
        // Active/click effects
        ':active': {
          transform: 'translateY(1px)',
        },
      }}
      // Inline styles for hover and active states (for demonstration)
      onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#c82333'}
      onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#dc3545'}
      onMouseDown={(e) => e.currentTarget.style.transform = 'translateY(1px)'}
      onMouseUp={(e) => e.currentTarget.style.transform = 'translateY(0)'}
    >
      Sign Out
    </button>
  );
};

export default SignOutButton;