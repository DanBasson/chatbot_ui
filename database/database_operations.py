"""
Database operations for the chatbot application using Supabase.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from .supabase_client import get_supabase_client
from static import (
    CHAT_SESSIONS_TABLE, CHAT_MESSAGES_TABLE, SESSION_ID_COLUMN, 
    USER_ID_COLUMN, SESSION_NAME_COLUMN, MESSAGE_ID_COLUMN, ROLE_COLUMN,
    CONTENT_COLUMN, METADATA_COLUMN, TIMESTAMP_COLUMN, CREATED_AT_COLUMN,
    UPDATED_AT_COLUMN, DEFAULT_USER_ID, DEFAULT_SESSION_NAME_TEMPLATE,
    DEFAULT_TIMESTAMP_FORMAT, USER_ROLE, ASSISTANT_ROLE,
    ERROR_CREATING_SESSION, ERROR_SAVING_MESSAGE, ERROR_RETRIEVING_HISTORY,
    ERROR_RETRIEVING_SESSIONS, ERROR_DELETING_SESSION, ERROR_UPDATING_METADATA
)



class ChatDatabase:
    """Handles all database operations for chat data."""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    def create_chat_session(self, user_id: Optional[str] = None, session_name: Optional[str] = None) -> str:
        """
        Create a new chat session.
        
        Args:
            user_id: Optional user identifier
            session_name: Optional session name
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        
        session_data = {
            SESSION_ID_COLUMN: session_id,
            USER_ID_COLUMN: user_id or DEFAULT_USER_ID,
            SESSION_NAME_COLUMN: session_name or DEFAULT_SESSION_NAME_TEMPLATE.format(timestamp=datetime.now().strftime(DEFAULT_TIMESTAMP_FORMAT)),
            CREATED_AT_COLUMN: datetime.now().isoformat(),
            UPDATED_AT_COLUMN: datetime.now().isoformat()
        }
        
        try:
            self.client.table(CHAT_SESSIONS_TABLE).insert(session_data).execute()
            return session_id
        except Exception as e:
            print(ERROR_CREATING_SESSION.format(error=e))
            raise
    
    def save_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict] = None) -> str:
        """
        Save a chat message to the database.
        
        Args:
            session_id: Chat session ID
            role: Message role ('user' or 'assistant')
            content: Message content
            metadata: Optional additional metadata
            
        Returns:
            Message ID
        """
        message_id = str(uuid.uuid4())
        
        message_data = {
            MESSAGE_ID_COLUMN: message_id,
            SESSION_ID_COLUMN: session_id,
            ROLE_COLUMN: role,
            CONTENT_COLUMN: content,
            METADATA_COLUMN: metadata or {},
            TIMESTAMP_COLUMN: datetime.now().isoformat()
        }
        
        try:
            self.client.table(CHAT_MESSAGES_TABLE).insert(message_data).execute()
            # Update session updated_at
            self.client.table(CHAT_SESSIONS_TABLE).update({
                UPDATED_AT_COLUMN: datetime.now().isoformat()
            }).eq(SESSION_ID_COLUMN, session_id).execute()
            
            return message_id
        except Exception as e:
            print(ERROR_SAVING_MESSAGE.format(error=e))
            raise
    
    def get_chat_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve chat history for a session.
        
        Args:
            session_id: Chat session ID
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of messages
        """
        try:
            response = self.client.table(CHAT_MESSAGES_TABLE).select('*').eq(
                SESSION_ID_COLUMN, session_id
            ).order(TIMESTAMP_COLUMN, desc=False).limit(limit).execute()
            
            return response.data
        except Exception as e:
            print(ERROR_RETRIEVING_HISTORY.format(error=e))
            raise
    
    def get_user_sessions(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get all chat sessions for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of sessions to retrieve
            
        Returns:
            List of sessions
        """
        try:
            response = self.client.table(CHAT_SESSIONS_TABLE).select('*').eq(
                USER_ID_COLUMN, user_id
            ).order(UPDATED_AT_COLUMN, desc=True).limit(limit).execute()
            
            return response.data
        except Exception as e:
            print(ERROR_RETRIEVING_SESSIONS.format(error=e))
            raise
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a chat session and all its messages.
        
        Args:
            session_id: Session ID to delete
            
        Returns:
            Success status
        """
        try:
            # Delete messages first
            self.client.table(CHAT_MESSAGES_TABLE).delete().eq(SESSION_ID_COLUMN, session_id).execute()
            # Delete session
            self.client.table(CHAT_SESSIONS_TABLE).delete().eq(SESSION_ID_COLUMN, session_id).execute()
            return True
        except Exception as e:
            print(ERROR_DELETING_SESSION.format(error=e))
            return False
    
    def update_session_metadata(self, session_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update session metadata.
        
        Args:
            session_id: Session ID
            metadata: Metadata to update
            
        Returns:
            Success status
        """
        try:
            update_data = {
                METADATA_COLUMN: metadata,
                UPDATED_AT_COLUMN: datetime.now().isoformat()
            }
            self.client.table(CHAT_SESSIONS_TABLE).update(update_data).eq(SESSION_ID_COLUMN, session_id).execute()
            return True
        except Exception as e:
            print(ERROR_UPDATING_METADATA.format(error=e))
            return False


# Convenience functions
def save_chat_interaction(session_id: str, user_message: str, assistant_response: str) -> tuple[str, str]:
    """
    Save a complete chat interaction (user message + assistant response).
    
    Args:
        session_id: Chat session ID
        user_message: User's message
        assistant_response: Assistant's response
        
    Returns:
        Tuple of (user_message_id, assistant_message_id)
    """
    db = ChatDatabase()
    user_msg_id = db.save_message(session_id, USER_ROLE, user_message)
    assistant_msg_id = db.save_message(session_id, ASSISTANT_ROLE, assistant_response)
    return user_msg_id, assistant_msg_id


def create_new_chat() -> str:
    """
    Create a new chat session with default settings.
    
    Returns:
        New session ID
    """
    db = ChatDatabase()
    return db.create_chat_session()