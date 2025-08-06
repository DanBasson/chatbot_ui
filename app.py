import streamlit as st
import threading
import queue##

from static import HEADER_CSS
from chat_logic import create_chat_handler

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

        # Create chat handler and necessary objects
        chat_handler = create_chat_handler()
        token_queue = queue.Queue()
        response_ready_event = threading.Event()

        # Start chat processing in background thread
        chat_handler.start_chat_thread(user_input, token_queue, response_ready_event)

        # Process streaming response and update UI
        rendered_text = chat_handler.process_streaming_response(
            response_placeholder, token_queue, response_ready_event
        )

        st.session_state.history.append({"role": "assistant", "content": rendered_text})
