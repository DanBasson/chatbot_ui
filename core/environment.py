"""
Environment detection utilities for the chatbot application.
"""

import os
from static import LOCAL_ENVIRONMENT, CLOUD_ENVIRONMENT


def get_environment() -> str:
    """
    Detect the current environment based on environment variables.
    
    Returns:
        Environment identifier ('local' or 'cloud')
    """
    # Streamlit Cloud sets this environment variable
    if os.getenv('STREAMLIT_SHARING_MODE') or os.getenv('STREAMLIT_CLOUD'):
        return CLOUD_ENVIRONMENT
    
    # Check if running in a typical cloud environment
    if any(os.getenv(var) for var in ['DYNO', 'RAILWAY_ENVIRONMENT', 'VERCEL']):
        return CLOUD_ENVIRONMENT
    
    # Default to local environment
    return LOCAL_ENVIRONMENT


def get_environment_prefix() -> str:
    """
    Get a prefix for session names based on environment.
    
    Returns:
        Environment prefix string
    """
    env = get_environment()
    return f"[{env.upper()}]"