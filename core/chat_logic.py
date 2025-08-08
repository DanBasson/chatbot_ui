import threading
import queue
import time
from typing import Callable, Optional
from langchain.callbacks.base import BaseCallbackHandler
from static.constants import (
    SIMULATED_TOKENS, LOADING_DOTS, CHAT_SIMULATION_DELAY, 
    TOKEN_DELAY, QUEUE_TIMEOUT, USER_ROLE, ASSISTANT_ROLE
)


class CollectTokensHandler(BaseCallbackHandler):
    """Token collector that adds tokens to the queue"""
    def __init__(self, token_queue: queue.Queue):
        self.token_queue = token_queue
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.token_queue.put(token)


class ChatHandler:
    """Handles chat logic and streaming responses"""
    
    def __init__(self):
        self.token_queue = None
        self.response_ready_event = None
        
    def run_chat_simulation(self, user_input: str) -> None:
        """Simulates chat response with Hebrew tokens"""
        time.sleep(CHAT_SIMULATION_DELAY)
        for token in SIMULATED_TOKENS:
            self.token_queue.put(token)
            time.sleep(TOKEN_DELAY)
        self.response_ready_event.set()
        
        # TODO: Replace with actual LLM integration
        # text = get_text_logic(user_input)
        # messages = [HumanMessage(content=text)]
        # chat(messages)
        # self.response_ready_event.set()
    
    def start_chat_thread(self, user_input: str, token_queue: queue.Queue, response_ready_event: threading.Event) -> None:
        """Starts the chat processing in a separate thread"""
        self.token_queue = token_queue
        self.response_ready_event = response_ready_event
        
        chat_thread = threading.Thread(target=self.run_chat_simulation, args=(user_input,))
        chat_thread.start()
    
    def process_streaming_response(self, response_placeholder, token_queue: queue.Queue, response_ready_event: threading.Event) -> str:
        """Processes the streaming response and updates the UI placeholder"""
        i = 0
        rendered_text = ""
        rendering_started = False

        while not response_ready_event.is_set() or not token_queue.empty():
            try:
                token = token_queue.get(timeout=QUEUE_TIMEOUT)
                rendered_text += token
                response_placeholder.markdown(rendered_text)
                rendering_started = True
            except queue.Empty:
                if not rendering_started:
                    response_placeholder.markdown(LOADING_DOTS[i % len(LOADING_DOTS)])
                    i += 1

                else:
                    response_placeholder.markdown(rendered_text)

        
        response_placeholder.markdown(rendered_text)
        return rendered_text


class ChatHandlerWithDatabase(ChatHandler):
    """Enhanced ChatHandler that saves conversations to database"""
    
    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id
        self._db = None
        
    @property
    def db(self):
        """Lazy load database to avoid import issues"""
        if self._db is None:
            from database import ChatDatabase
            self._db = ChatDatabase()
        return self._db
    
    def run_chat_simulation(self, user_input: str) -> None:
        """Simulates chat response and saves to database"""
        time.sleep(CHAT_SIMULATION_DELAY)
        
        full_response = ""
        for token in SIMULATED_TOKENS:
            self.token_queue.put(token)
            full_response += token
            time.sleep(TOKEN_DELAY)
        
        # Save the complete interaction to database
        try:
            # Save user message
            self.db.save_message(self.session_id, USER_ROLE, user_input)
            # Save assistant response  
            self.db.save_message(self.session_id, ASSISTANT_ROLE, full_response)
            print(f"💾 Saved interaction to database (session: {self.session_id[:8]}...)")
        except Exception as e:
            print(f"❌ Failed to save to database: {e}")
        
        self.response_ready_event.set()


def create_chat_handler() -> ChatHandler:
    """Factory function to create a ChatHandler instance"""
    return ChatHandler()


def create_chat_handler_with_db(session_id: str) -> ChatHandlerWithDatabase:
    """Factory function to create a ChatHandlerWithDatabase instance"""
    return ChatHandlerWithDatabase(session_id)