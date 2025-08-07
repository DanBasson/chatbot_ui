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
        self.url = os.getenv(SUPABASE_URL_ENV)
        self.key = os.getenv(SUPABASE_KEY_ENV)
        
    def connect(self) -> Client:
        """Initialize and return Supabase client."""
        if not self.url or not self.key:
            raise ValueError(ERROR_SUPABASE_CREDENTIALS)
        
        if self.client is None:
            self.client = create_client(self.url, self.key)
        
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