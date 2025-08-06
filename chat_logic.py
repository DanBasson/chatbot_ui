import threading
import queue
import time
from typing import Callable
from langchain.callbacks.base import BaseCallbackHandler


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
        simulated_tokens = ["שלום", " ", "**לך**", ",", " ", "מה", " ", "שלומך", "?"]
        time.sleep(1.6)
        for token in simulated_tokens:
            self.token_queue.put(token)
            time.sleep(0.1)
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
        dots = [" •", " ••", " •••", " ••••"]
        i = 0
        rendered_text = ""
        rendering_started = False
        print('========')
        
        while not response_ready_event.is_set() or not token_queue.empty():
            try:
                token = token_queue.get(timeout=0.3)
                print(1111)
                rendered_text += token
                response_placeholder.markdown(rendered_text)
                rendering_started = True
            except queue.Empty:
                if not rendering_started:
                    response_placeholder.markdown(dots[i % len(dots)])
                    i += 1
                    print(222)
                else:
                    response_placeholder.markdown(rendered_text)
                    print(333)
        
        response_placeholder.markdown(rendered_text)
        return rendered_text


def create_chat_handler() -> ChatHandler:
    """Factory function to create a ChatHandler instance"""
    return ChatHandler()