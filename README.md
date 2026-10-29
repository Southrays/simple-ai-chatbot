# Simple AI Chatbot

A simple AI chatbot built with **FastAPI, LangChain, and LangGraph**. The application provides a REST API for interacting with an AI assistant and supports conversation memory using LangGraph's in-memory checkpointing.

## Features

- AI-powered chatbot using LangChain.
- FastAPI REST API.
- Conversation memory using LangGraph `InMemorySaver`.
- Unique conversation IDs for managing chat sessions.
- Pydantic request and response validation.
- Centralized application logging.
- Error handling for AI service failures.
- Automated API tests using pytest.

## Tech Stack

- **Python 3.12**
- **FastAPI** – API framework
- **LangChain** – AI agent orchestration
- **LangGraph** – Conversation state and memory
- **OpenAI** – Language model
- **Pydantic** – Data validation
- **SQLAlchemy** – Database toolkit
- **pytest** – Testing
- **uv** – Python package and project management


## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/simple-chatbot.git
```

### 2. Navigate to the backend

```bash
cd simple-chatbot/backend
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Configure environment variables

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key
```

### 5. Run the application

```bash
uv run uvicorn api_layer.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/chat/` | Send a message to the chatbot |


## Running Tests

Run the test suite:

```bash
uv run pytest tests/ -v
```

The tests cover:

- Chat endpoint responses.
- Conversation ID generation.
- Existing conversation ID handling.
- Request validation.
- AI service error handling.
- Health endpoint responses.

## Memory

Conversation memory is currently managed using LangGraph's `InMemorySaver`.

Each conversation is associated with a unique conversation ID.

**Note:** Conversation memory is temporary and is lost when the application process restarts. It is not currently backed by persistent database storage.