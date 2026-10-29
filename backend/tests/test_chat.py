from unittest.mock import AsyncMock, patch
from uuid import UUID

from api_layer.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_chat_creates_new_conversation_id():
    with patch(
        "api_layer.routes.chat.send_message",
        new_callable=AsyncMock,
    ) as mock_send_message:
        mock_send_message.return_value = "Hello!"

        response = client.post(
            "/chat/",
            json={"user_input": "Hello"},
        )
        print(response.json())

    assert response.status_code == 200

    data = response.json()
    assert data["response"] == "Hello!"
    assert "conversation_id" in data

    # Confirm the generated ID is a valid UUID.
    UUID(data["conversation_id"])

    # Confirm the generated ID was passed to the AI layer.
    mock_send_message.assert_awaited_once_with(
        "Hello",
        data["conversation_id"],
    )


def test_chat_reuses_existing_conversation_id():
    conversation_id = "test-conversation-123"

    with patch(
        "api_layer.routes.chat.send_message",
        new_callable=AsyncMock,
    ) as mock_send_message:
        mock_send_message.return_value = "Your name is Alex."

        response = client.post(
            "/chat/",
            json={
                "user_input": "What is my name?",
                "conversation_id": conversation_id,
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "response": "Your name is Alex.",
        "conversation_id": conversation_id,
    }

    mock_send_message.assert_awaited_once_with(
        "What is my name?",
        conversation_id,
    )


def test_chat_rejects_empty_message():
    response = client.post(
        "/chat/",
        json={"user_input": ""},
    )

    assert response.status_code == 422


def test_chat_rejects_excessively_long_message():
    response = client.post(
        "/chat/",
        json={"user_input": "a" * 4001},
    )

    assert response.status_code == 422


def test_chat_handles_value_error():
    with patch(
        "api_layer.routes.chat.send_message",
        new_callable=AsyncMock,
    ) as mock_send_message:
        mock_send_message.side_effect = ValueError(
            "Internal configuration details"
        )

        response = client.post(
            "/chat/",
            json={"user_input": "Hello"},
        )
        print(response.json())

    assert response.status_code == 502
    assert response.json() == {
        "detail": "The AI service could not complete your request."
    }
    assert "Internal configuration details" not in response.text
