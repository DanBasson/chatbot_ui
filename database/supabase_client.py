"""
Supabase client configuration for the chatbot application.
"""

import os
from typing import Optional
from supabase import create_client, Client
from static import SUPABASE_URL_ENV, SUPABASE_KEY_ENV, ERROR_SUPABASE_CREDENTIALS


class SupabaseClient:
    """Supabase client wrapper for database operations."""
    
    def __init__(self):
        self.client: Optional[Client] = None
        
    def connect(self) -> Client:
        """Initialize and return Supabase client."""
        # Get environment variables when connecting, not during initialization
        url = os.getenv(SUPABASE_URL_ENV)
        key = os.getenv(SUPABASE_KEY_ENV)
        
        if not url or not key:
            raise ValueError(ERROR_SUPABASE_CREDENTIALS)
        
        if self.client is None:
            self.client = create_client(url, key)
        
        return self.client
    
    def get_client(self) -> Client:
        """Get the Supabase client, connecting if necessary."""
        if self.client is None:
            return self.connect()
        return self.client


# Global instance
supabase_client = SupabaseClient()


def get_supabase_client() -> Client:
    """Get the global Supabase client instance."""
    return supabase_client.get_client()