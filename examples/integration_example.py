"""
Example of how to integrate the Supabase database operations with the existing chatbot.
This shows how to modify your chat_logic.py to save conversations to the database.
"""

import threading
import queue
import time
from typing import Callable
from langchain.callbacks.base import BaseCallbackHandler
from database_operations import ChatDatabase, save_chat_interaction


class CollectTokensHandler(BaseCallbackHandler):
    """Token collector that adds tokens to the queue"""
    def __init__(self, token_queue: queue.Queue):
        self.token_queue = token_queue
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.token_queue.put(token)


class ChatHandlerWithDatabase:
    """Enhanced ChatHandler that saves conversations to Supabase"""
    
    def __init__(self, session_id: str = None):
        self.token_queue = None
        self.response_ready_event = None
        self.db = ChatDatabase()
        
        # Create or use existing session
        if session_id:
            self.session_id = session_id
        else:
            self.session_id = self.db.create_chat_session()
        
    def run_chat_simulation(self, user_input: str) -> str:
        """Simulates chat response with Hebrew tokens and saves to database"""
        simulated_tokens = ["שלום", " ", "**לך**", ",", " ", "מה", " ", "שלומך", "?"]
        time.sleep(1.6)
        
        full_response = ""
        for token in simulated_tokens:
            self.token_queue.put(token)
            full_response += token
            time.sleep(0.1)
        
        # Save the complete interaction to database
        try:
            save_chat_interaction(self.session_id, user_input, full_response)
            print(f"💾 Saved interaction to database (session: {self.session_id[:8]}...)")
        except Exception as e:
            print(f"❌ Failed to save to database: {e}")
        
        self.response_ready_event.set()
        return full_response
        
    def start_chat_thread(self, user_input: str, token_queue: queue.Queue, response_ready_event: threading.Event) -> None:
        """Starts the chat processing in a separate thread"""
        self.token_queue = token_queue
        self.response_ready_event = response_ready_event
        
        chat_thread = threading.Thread(target=self.run_chat_simulation, args=(user_input,))
        chat_thread.start()
    
    def process_streaming_response(self, response_placeholder, token_queue: queue.Queue, response_ready_event: threading.Event) -> str:
        """Processes the streaming response and updates the UI placeholder"""
        dots = [" •", " ••", " •••", " ••••"]
        i = 0
        rendered_text = ""
        rendering_started = False
        
        while not response_ready_event.is_set() or not token_queue.empty():
            try:
                token = token_queue.get(timeout=0.3)
                rendered_text += token
                response_placeholder.markdown(rendered_text)
                rendering_started = True
            except queue.Empty:
                if not rendering_started:
                    response_placeholder.markdown(dots[i % len(dots)])
                    i += 1
                else:
                    response_placeholder.markdown(rendered_text)
        
        response_placeholder.markdown(rendered_text)
        return rendered_text
    
    def get_chat_history(self, limit: int = 50):
        """Get chat history for the current session"""
        return self.db.get_chat_history(self.session_id, limit)
    
    def get_session_id(self) -> str:
        """Get the current session ID"""
        return self.session_id


def create_chat_handler_with_db(session_id: str = None) -> ChatHandlerWithDatabase:
    """Factory function to create a ChatHandlerWithDatabase instance"""
    return ChatHandlerWithDatabase(session_id)


# Example usage in a Streamlit app
def example_streamlit_integration():
    """
    Example of how to modify your app.py to use database integration.
    
    Replace the relevant parts of your app.py with this code:
    """
    
    example_code = '''
import streamlit as st
import threading
import queue
import os

from static import HEADER_CSS
from integration_example import create_chat_handler_with_db

# Set environment variables (in production, use st.secrets or environment)
# os.environ['SUPABASE_URL'] = 'your-supabase-url'
# os.environ['SUPABASE_KEY'] = 'your-supabase-key'

st.set_page_config(page_title="ג'אקו צ'אט")
st.markdown(HEADER_CSS, unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
    
if "chat_handler" not in st.session_state:
    # Create a chat handler with database integration
    st.session_state.chat_handler = create_chat_handler_with_db()
    st.session_state.session_id = st.session_state.chat_handler.get_session_id()

# Display current session info
st.sidebar.write(f"Session ID: {st.session_state.session_id[:8]}...")

# Load chat history from database if history is empty
if not st.session_state.history:
    try:
        db_history = st.session_state.chat_handler.get_chat_history()
        for msg in db_history:
            st.session_state.history.append({
                "role": msg["role"], 
                "content": msg["content"]
            })
    except Exception as e:
        st.sidebar.error(f"Failed to load history: {e}")

# Rest of your existing chat UI code...
# (The chat processing will automatically save to database)
    '''
    
    return example_code


if __name__ == "__main__":
    print("Database Integration Example")
    print("="*50)
    
    print("1. Enhanced ChatHandler with database integration created")
    print("2. Example Streamlit integration code available")
    print("3. To use in your app:")
    print("   - Replace 'from chat_logic import create_chat_handler'")
    print("   - With 'from integration_example import create_chat_handler_with_db'")
    print("   - Set your SUPABASE_URL and SUPABASE_KEY environment variables")
    
    print("\nExample Streamlit integration code:")
    print("="*50)
    print(example_streamlit_integration())