import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from ai_layer import chatbot_with_database as chatbot


def test_send_message_includes_saved_memories(monkeypatch):
    saved_memories = [
        SimpleNamespace(memory="I am learning AI engineering."),
        SimpleNamespace(memory="I use Python and FastAPI."),
    ]

    monkeypatch.setattr(
        chatbot,
        "get_user_memories",
        lambda user_id: saved_memories,
    )

    agent = SimpleNamespace(
        ainvoke=AsyncMock(
            return_value={
                "messages": [
                    SimpleNamespace(text="You are learning AI engineering.")
                ]
            }
        )
    )

    response = asyncio.run(
        chatbot.send_message(
            agent=agent,
            user_input="What am I learning?",
            conversation_id="conversation_123",
            user_id="user_123",
        )
    )

    assert response == "You are learning AI engineering."

    agent.ainvoke.assert_awaited_once()

    invocation = agent.ainvoke.await_args
    message_content = invocation.args[0]["messages"][0].content

    assert "I am learning AI engineering." in message_content
    assert "I use Python and FastAPI." in message_content
    assert "What am I learning?" in message_content


def test_send_message_saves_new_memory(monkeypatch):
    saved_facts = []

    def mock_save_memory(user_id, memory):
        saved_facts.append((user_id, memory))

    monkeypatch.setattr(
        chatbot,
        "save_user_memory",
        mock_save_memory,
    )

    monkeypatch.setattr(
        chatbot,
        "get_user_memories",
        lambda user_id: [],
    )

    agent = SimpleNamespace(
        ainvoke=AsyncMock(
            return_value={
                "messages": [
                    SimpleNamespace(text="I'll remember that.")
                ]
            }
        )
    )

    response = asyncio.run(
        chatbot.send_message(
            agent=agent,
            user_input="Remember that I am learning LangGraph.",
            conversation_id="conversation_123",
            user_id="user_123",
        )
    )

    assert response == "I'll remember that."

    assert saved_facts == [
        ("user_123", "I am learning LangGraph.")
    ]


def test_send_message_does_not_save_unrelated_messages(monkeypatch):
    save_memory_mock = AsyncMock()

    monkeypatch.setattr(
        chatbot,
        "save_user_memory",
        save_memory_mock,
    )

    monkeypatch.setattr(
        chatbot,
        "get_user_memories",
        lambda user_id: [],
    )

    agent = SimpleNamespace(
        ainvoke=AsyncMock(
            return_value={
                "messages": [
                    SimpleNamespace(text="Hello!")
                ]
            }
        )
    )

    asyncio.run(
        chatbot.send_message(
            agent=agent,
            user_input="Hello, how are you?",
            conversation_id="conversation_123",
            user_id="user_123",
        )
    )

    save_memory_mock.assert_not_called()


def test_send_message_propagates_agent_errors(monkeypatch):
    monkeypatch.setattr(
        chatbot,
        "get_user_memories",
        lambda user_id: [],
    )

    agent = SimpleNamespace(
        ainvoke=AsyncMock(
            side_effect=RuntimeError("AI service unavailable")
        )
    )

    with pytest.raises(RuntimeError):
        asyncio.run(
            chatbot.send_message(
                agent=agent,
                user_input="Hello",
                conversation_id="conversation_123",
                user_id="user_123",
            )
        )