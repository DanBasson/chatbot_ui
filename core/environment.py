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
    # Check for Streamlit Cloud environment variables (multiple possible names)
    streamlit_cloud_vars = [
        'STREAMLIT_SHARING_MODE', 
        'STREAMLIT_CLOUD',
        'STREAMLIT_SERVER_PORT',  # Streamlit Cloud often sets this
        'STREAMLIT_RUNTIME_MAX_CACHED_MESSAGE_AGE'  # Another Streamlit Cloud indicator
    ]
    
    if any(os.getenv(var) for var in streamlit_cloud_vars):
        return CLOUD_ENVIRONMENT
    
    # Check if running in a typical cloud environment
    if any(os.getenv(var) for var in ['DYNO', 'RAILWAY_ENVIRONMENT', 'VERCEL']):
        return CLOUD_ENVIRONMENT
    
    # Check if path indicates cloud environment
    if '/mount/src/' in os.getcwd():  # Streamlit Cloud mounts apps here
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