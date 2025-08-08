"""Static configuration module containing all application constants."""

from .constants import *

__all__ = [
    # Session State Keys
    'HISTORY_KEY', 'CHAT_HANDLER_KEY', 'SESSION_ID_KEY', 'TOKEN_BUFFER_KEY',
    
    # UI Text and Labels
    'PAGE_TITLE', 'CHAT_INPUT_PLACEHOLDER', 'SIGNATURE_TEXT',
    
    # Message Roles
    'USER_ROLE', 'ASSISTANT_ROLE',
    
    # Database Constants
    'CHAT_SESSIONS_TABLE', 'CHAT_MESSAGES_TABLE',
    'SESSION_ID_COLUMN', 'USER_ID_COLUMN', 'SESSION_NAME_COLUMN',
    'MESSAGE_ID_COLUMN', 'ROLE_COLUMN', 'CONTENT_COLUMN',
    'METADATA_COLUMN', 'TIMESTAMP_COLUMN', 'CREATED_AT_COLUMN', 'UPDATED_AT_COLUMN',
    
    # Environment Variables
    'SUPABASE_URL_ENV', 'SUPABASE_KEY_ENV',
    
    # Default Values
    'DEFAULT_USER_ID', 'DEFAULT_SESSION_NAME_TEMPLATE', 'DEFAULT_TIMESTAMP_FORMAT',
    
    # Chat Simulation
    'SIMULATED_TOKENS', 'LOADING_DOTS',
    
    # Timing Configurations
    'CHAT_SIMULATION_DELAY', 'TOKEN_DELAY', 'QUEUE_TIMEOUT',
    
    # Error Messages
    'ERROR_CREATING_SESSION', 'ERROR_SAVING_MESSAGE', 'ERROR_RETRIEVING_HISTORY',
    'ERROR_RETRIEVING_SESSIONS', 'ERROR_DELETING_SESSION', 'ERROR_UPDATING_METADATA',
    'ERROR_SUPABASE_CREDENTIALS',
    
    # SQL Queries
    'CREATE_CHAT_SESSIONS_SQL', 'CREATE_CHAT_MESSAGES_SQL', 'INDEXES_SQL',
    
    # UI Styling
    'FONTS_URL',

]