# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hebrew-language Streamlit chat application that simulates streaming LLM responses with a right-to-left (RTL) UI. The project includes both production and development/testing versions.

## Key Files

- `app.py` - Main Streamlit chat application with Hebrew UI and simulated streaming
- `app_with_mockup_text.py` - Alternative version (similar to app.py with minor differences)
- `static.py` - Contains CSS styling for Hebrew RTL layout and signature animation
- `draft.py` - Contains API key and LangChain/Groq integration code (development/testing)
- `mock_llm.py` - LangChain streaming examples and demos (incomplete, references missing MockStreamingLLM class)

## Development Commands

To run the main application:
```bash
streamlit run app.py
```

To run the alternative version:
```bash
streamlit run app_with_mockup_text.py
```

## Architecture

### Core Components

1. **Streamlit UI**: Uses Hebrew text and RTL layout with custom CSS from `static.py`
2. **Threading**: Implements producer-consumer pattern with `queue.Queue()` and `threading.Event()` for simulated streaming
3. **Session State**: Manages chat history in `st.session_state.history`
4. **LangChain Integration**: Prepared for real LLM integration via `CollectTokensHandler` callback

### Streaming Implementation

The app uses a multi-threaded approach:
- Main thread handles UI updates and token rendering
- Background thread (`run_chat()`) simulates LLM token generation
- Communication via `token_queue` (Queue) and `response_ready_event` (threading.Event)

### UI Features

- Hebrew interface with RTL text alignment
- Animated signature using SVG and CSS keyframes
- Loading dots animation while waiting for responses
- Real-time token streaming display

## Important Notes

- **API Keys**: The `draft.py` file contains a Groq API key that should be moved to environment variables
- **Dependencies**: Project uses Streamlit, LangChain, and threading for core functionality
- **Language**: All user-facing text is in Hebrew
- **Virtual Environment**: Uses `.venv/` (Python virtual environment present)

## Security Considerations

- Move API keys from `draft.py` to environment variables or secrets management
- The current Groq API key in `draft.py` should be rotated for security