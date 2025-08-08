"""
Application constants for the chatbot project.
All string literals and configuration values are centralized here.
"""

# ==============================
# SESSION STATE KEYS
# ==============================
HISTORY_KEY = "history"
CHAT_HANDLER_KEY = "chat_handler"
SESSION_ID_KEY = "session_id"
TOKEN_BUFFER_KEY = "token_buffer"

# ==============================
# UI TEXT AND LABELS (Hebrew)
# ==============================
PAGE_TITLE = "ג'אקו צ'אט"
CHAT_INPUT_PLACEHOLDER = "השאלה שלי..."
SIGNATURE_TEXT = "הסוכן החכם של ג'אקו"

# ==============================
# MESSAGE ROLES
# ==============================
USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"

# ==============================
# DATABASE TABLE NAMES
# ==============================
CHAT_SESSIONS_TABLE = "chat_sessions"
CHAT_MESSAGES_TABLE = "chat_messages"

# ==============================
# DATABASE COLUMN NAMES
# ==============================
SESSION_ID_COLUMN = "session_id"
USER_ID_COLUMN = "user_id"
SESSION_NAME_COLUMN = "session_name"
MESSAGE_ID_COLUMN = "message_id"
ROLE_COLUMN = "role"
CONTENT_COLUMN = "content"
METADATA_COLUMN = "metadata"
TIMESTAMP_COLUMN = "timestamp"
CREATED_AT_COLUMN = "created_at"
UPDATED_AT_COLUMN = "updated_at"

# ==============================
# ENVIRONMENT VARIABLES
# ==============================
SUPABASE_URL_ENV = "SUPABASE_URL"
SUPABASE_KEY_ENV = "SUPABASE_KEY"

# ==============================
# DEFAULT VALUES
# ==============================
DEFAULT_USER_ID = "anonymous"
DEFAULT_SESSION_NAME_TEMPLATE = "Chat Session {timestamp}"
DEFAULT_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"

# ==============================
# ENVIRONMENT DETECTION
# ==============================
ENVIRONMENT_COLUMN = "environment"
LOCAL_ENVIRONMENT = "local"
CLOUD_ENVIRONMENT = "cloud"

# ==============================
# TIMEZONE SETTINGS
# ==============================
TURKEY_TIMEZONE = "Europe/Istanbul"

# ==============================
# CHAT SIMULATION
# ==============================
SIMULATED_TOKENS = ["שלום", " ", "**לך**", ",", " ", "מה", " ", "שלומך", "?"]
LOADING_DOTS = [" •", " ••", " •••", " ••••"]

# ==============================
# TIMING CONFIGURATIONS
# ==============================
CHAT_SIMULATION_DELAY = 1.6
TOKEN_DELAY = 0.1
QUEUE_TIMEOUT = 0.3

# ==============================
# ERROR MESSAGES
# ==============================
ERROR_CREATING_SESSION = "Error creating chat session: {error}"
ERROR_SAVING_MESSAGE = "Error saving message: {error}"
ERROR_RETRIEVING_HISTORY = "Error retrieving chat history: {error}"
ERROR_RETRIEVING_SESSIONS = "Error retrieving user sessions: {error}"
ERROR_DELETING_SESSION = "Error deleting session: {error}"
ERROR_UPDATING_METADATA = "Error updating session metadata: {error}"
ERROR_SUPABASE_CREDENTIALS = "Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_KEY environment variables."

# ==============================
# SQL QUERIES
# ==============================
CREATE_CHAT_SESSIONS_SQL = """
    CREATE TABLE IF NOT EXISTS chat_sessions (
        id SERIAL PRIMARY KEY,
        session_id UUID UNIQUE NOT NULL,
        user_id TEXT NOT NULL DEFAULT 'anonymous',
        session_name TEXT NOT NULL,
        environment TEXT NOT NULL DEFAULT 'local',
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
"""

CREATE_CHAT_MESSAGES_SQL = """
    CREATE TABLE IF NOT EXISTS chat_messages (
        id SERIAL PRIMARY KEY,
        message_id UUID UNIQUE NOT NULL,
        session_id UUID NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
        content TEXT NOT NULL,
        environment TEXT NOT NULL DEFAULT 'local',
        metadata JSONB DEFAULT '{}',
        timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
    );
"""

# ==============================
# DATABASE INDEXES
# ==============================
INDEXES_SQL = [
    "CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id);",
    "CREATE INDEX IF NOT EXISTS idx_chat_sessions_updated_at ON chat_sessions(updated_at);",
    "CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);",
    "CREATE INDEX IF NOT EXISTS idx_chat_messages_timestamp ON chat_messages(timestamp);"
]

# ==============================
# UI STYLING
# ==============================
FONTS_URL = "https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap"

