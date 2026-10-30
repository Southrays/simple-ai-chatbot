from api_layer.routes import chat_with_database
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
app.include_router(chat_with_database.router)

app.state.agent = object()

client = TestClient(
    app,
    raise_server_exceptions=False,
)


def test_chat_endpoint_successfully_processes_request(monkeypatch):
    async def mock_send_message(
        agent,
        user_input,
        conversation_id,
        user_id,
    ):
        assert user_input == "Hello"
        assert user_id == "user_123"
        assert conversation_id == "conversation_123"

        return "Hello! How can I help you?"

    monkeypatch.setattr(
        chat_with_database,
        "send_message",
        mock_send_message,
    )

    response = client.post(
        "/chat_with_database/",
        json={
            "user_input": "Hello",
            "user_id": "user_123",
            "conversation_id": "conversation_123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response"] == "Hello! How can I help you?"
    assert data["conversation_id"] == "conversation_123"


def test_chat_endpoint_generates_conversation_id(monkeypatch):
    async def mock_send_message(
        agent,
        user_input,
        conversation_id,
        user_id,
    ):
        assert conversation_id is not None
        assert len(conversation_id) == 36

        return "Hello!"

    monkeypatch.setattr(
        chat_with_database,
        "send_message",
        mock_send_message,
    )

    response = client.post(
        "/chat_with_database/",
        json={
            "user_input": "Hello",
            "user_id": "user_123",
        },
    )

    assert response.status_code == 200
    assert response.json()["conversation_id"] is not None


def test_chat_endpoint_handles_ai_service_failure(monkeypatch):
    async def mock_send_message(
        agent,
        user_input,
        conversation_id,
        user_id,
    ):
        raise RuntimeError("AI service unavailable")

    monkeypatch.setattr(
        chat_with_database,
        "send_message",
        mock_send_message,
    )

    response = client.post(
        "/chat_with_database/",
        json={
            "user_input": "Hello",
            "user_id": "user_123",
        },
    )

    assert response.status_code == 502

    assert response.json()["detail"] == (
        "The AI service could not complete your request."
    )


def test_chat_endpoint_rejects_invalid_request():
    response = client.post(
        "/chat_with_database/",
        json={
            "user_input": "",
            "user_id": "user_123",
        },
    )

    assert response.status_code == 422