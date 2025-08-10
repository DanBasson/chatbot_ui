"""
Authentication module for Streamlit chatbot application.
Handles user login, logout, and session management.
"""

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from typing import Optional, Tuple


class AuthenticationManager:
    """Manages user authentication for the Streamlit app."""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize authentication manager with config file."""
        self.config_path = config_path
        self.authenticator = self._load_authenticator()
    
    def _load_authenticator(self) -> stauth.Authenticate:
        """Load and create authenticator from config file."""
        try:
            with open(self.config_path) as file:
                config = yaml.load(file, Loader=SafeLoader)
            
            return stauth.Authenticate(
                config['credentials'],
                config['cookie']['name'],
                config['cookie']['key'],
                config['cookie']['expiry_days'],
                auto_hash=False
            )
        except FileNotFoundError:
            st.error(f"❌ Authentication config file not found: {self.config_path}")
            st.stop()
        except Exception as e:
            st.error(f"❌ Error loading authentication config: {e}")
            st.stop()
    
    def render_login(self) -> None:
        """Render the Hebrew login form."""
        self.authenticator.login(
            location='main',
            fields={
                'Form name': 'כניסה למערכת',
                'Username': 'שם משתמש', 
                'Password': 'סיסמה',
                'Login': 'כניסה'
            }
        )
    
    def handle_authentication(self) -> bool:
        """
        Handle authentication logic and display appropriate messages.
        
        Returns:
            bool: True if user is authenticated, False otherwise
        """
        auth_status = st.session_state.get('authentication_status')
        
        if auth_status is False:
            st.error('🚫 שם משתמש או סיסמה שגויים')
            return False
        elif auth_status is None:
            st.warning('⚠️ אנא הזן את שם המשתמש והסיסמה שלך')
            return False
        elif auth_status:
            self._show_authenticated_ui()
            return True
        
        return False
    
    def _show_authenticated_ui(self) -> None:
        """Show logout button and welcome message for authenticated users."""
        # Render logout button
        self.authenticator.logout(button_name='התנתק', location='sidebar')
        
        # Show welcome message
        user_name = st.session_state.get("name", "משתמש")
        username = st.session_state.get("username", "")
        
        st.sidebar.write(f'ברוך הבא *{user_name}*')
        st.sidebar.write(f'👤 מחובר כ: {username}')
    
    def require_authentication(self) -> bool:
        """
        Complete authentication flow - render login and handle authentication.
        
        Returns:
            bool: True if user is authenticated, False if authentication failed
        """
        # Render login form
        self.render_login()
        
        # Handle authentication
        return self.handle_authentication()
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated."""
        return st.session_state.get('authentication_status', False)
    
    def get_current_user(self) -> Optional[Tuple[str, str]]:
        """
        Get current authenticated user information.
        
        Returns:
            Tuple of (name, username) or None if not authenticated
        """
        if self.is_authenticated():
            return (
                st.session_state.get("name"),
                st.session_state.get("username")
            )
        return None


# Convenience function for easy import
def get_auth_manager() -> AuthenticationManager:
    """Get singleton authentication manager instance."""
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = AuthenticationManager()
    return st.session_state.auth_manager