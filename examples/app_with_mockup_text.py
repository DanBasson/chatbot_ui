import json
import time
import datetime
from datetime import timedelta
import uuid
from functools import lru_cache
from typing import Optional, Dict, Any
import re
import streamlit as st
import threading
import queue
import time
import os, sys

from static import HEADER_CSS
from langchain.callbacks.base import BaseCallbackHandler




# Token collector that adds tokens to the queue
class CollectTokensHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        token_queue.put(token)


def send_token_to_ui(token_chunk):
    if "token_buffer" not in st.session_state:
        st.session_state.token_buffer = ""
    st.session_state.token_buffer += token_chunk
    time.sleep(1)
    response_placeholder.markdown(st.session_state.token_buffer)


st.set_page_config(page_title="ג'אקו צ'אט")
st.markdown(HEADER_CSS, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

chat_container = st.container()
with chat_container:
    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("השאלה שלי...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        response_placeholder = st.empty()
        dots = [" •", " ••", " •••", " ••••"]
        i = 0

        # Shared queue for passing tokens to UI thread
        token_queue = queue.Queue()
        response_ready_event = threading.Event()

        token_collector = CollectTokensHandler()
        # chat = get_chat_bedrock_instance(callbacks=[token_collector])


        def run_chat():
            simulated_tokens = ["שלום", " ", "**לך**", ",", " ", "מה", " ", "שלומך", "?"]
            time.sleep(1.4)
            for token in simulated_tokens:
                token_queue.put(token)
                time.sleep(0.4)
            response_ready_event.set()

            # text = get_text_logic(user_input)  # f"<system_prompt> {user_input} </system_prompt>\n\nAssistant:"
            # messages = [HumanMessage(content=text)]
            # chat(messages)
            # response_ready_event.set()


        threading.Thread(target=run_chat).start()

        # Show animated dots and render streamed tokens
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

        st.session_state.history.append({"role": "assistant", "content": rendered_text})
