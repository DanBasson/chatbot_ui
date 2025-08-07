import streamlit as st
import threading
import queue
from dotenv import load_dotenv

from core.chat_logic import create_chat_handler_with_db, create_chat_handler
from database import ChatDatabase
from static.ui import HEADER_CSS
from static import (
    PAGE_TITLE, CHAT_INPUT_PLACEHOLDER, HISTORY_KEY,
    USER_ROLE, ASSISTANT_ROLE, ROLE_COLUMN, CONTENT_COLUMN,
    SESSION_ID_KEY, CHAT_HANDLER_KEY
)

load_dotenv()

st.set_page_config(page_title=PAGE_TITLE)
st.markdown(HEADER_CSS, unsafe_allow_html=True)

if HISTORY_KEY not in st.session_state:
    st.session_state.history = []

if SESSION_ID_KEY not in st.session_state:
    try:
        # Create database instance and new chat session
        st.session_state.db = ChatDatabase()
        st.session_state.session_id = st.session_state.db.create_chat_session()
        st.success(f"🆕 New chat session started")
    except Exception as e:
        st.error(f"❌ Failed to create database session: {e}")
        st.session_state.session_id = None
        st.session_state.db = None

if CHAT_HANDLER_KEY not in st.session_state and st.session_state.session_id:
    try:
        st.session_state.chat_handler = create_chat_handler_with_db(st.session_state.session_id)

        # Load existing chat history from database
        db_history = st.session_state.db.get_chat_history(st.session_state.session_id)
        for msg in db_history:##
            st.session_state.history.append({
                ROLE_COLUMN: msg[ROLE_COLUMN],
                CONTENT_COLUMN: msg[CONTENT_COLUMN]
            })

        if db_history:
            st.info(f"📚 Loaded {len(db_history)} previous messages")

    except Exception as e:
        st.sidebar.error(f"Failed to load chat history: {e}")
        st.session_state.chat_handler = create_chat_handler()

# Display session info in sidebar
if st.session_state.session_id:
    st.sidebar.write(f"💬 Session: {st.session_state.session_id[:8]}")

    # Add button to start new conversation
    if st.sidebar.button("🆕 שיחה חדשה"):
        st.session_state.clear()
        st.rerun()

chat_container = st.container()
with chat_container:
    for message in st.session_state.history:
        with st.chat_message(message[ROLE_COLUMN]):
            st.markdown(message[CONTENT_COLUMN])

user_input = st.text_area(
    label="",
    placeholder=CHAT_INPUT_PLACEHOLDER,
    height=60,  # Two lines height
    key="user_input_area"
)

send_button = st.button("📤 שלח", key="send_button", type="primary")

if user_input and send_button:
    st.session_state.history.append({ROLE_COLUMN: USER_ROLE, CONTENT_COLUMN: user_input})

    with st.chat_message(USER_ROLE):
        st.markdown(user_input)

    with st.chat_message(ASSISTANT_ROLE):
        response_placeholder = st.empty()

        # Use existing chat handler or create fallback
        chat_handler = getattr(st.session_state, 'chat_handler', create_chat_handler())
        token_queue = queue.Queue()
        response_ready_event = threading.Event()

        # Start chat processing in background thread
        chat_handler.start_chat_thread(user_input, token_queue, response_ready_event)

        # Process streaming response and update UI
        rendered_text = chat_handler.process_streaming_response(
            response_placeholder, token_queue, response_ready_event
        )

        st.session_state.history.append({ROLE_COLUMN: ASSISTANT_ROLE, CONTENT_COLUMN: rendered_text})

        # Clear the input after sending
        st.session_state.user_input_area = ""


