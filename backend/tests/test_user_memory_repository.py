from database.models import UserMemory
from database.repositories import user_memory


def test_save_user_memory(test_session_factory, monkeypatch):
    monkeypatch.setattr(
        user_memory,
        "SessionLocal",
        test_session_factory,
    )

    result = user_memory.save_user_memory(
        user_id="user_123",
        memory="I am learning AI engineering.",
    )

    assert isinstance(result, UserMemory)
    assert result.user_id == "user_123"
    assert result.memory == "I am learning AI engineering."
    assert result.id is not None


def test_get_user_memories(test_session_factory, monkeypatch):
    monkeypatch.setattr(
        user_memory,
        "SessionLocal",
        test_session_factory,
    )

    user_memory.save_user_memory(
        user_id="user_123",
        memory="I am learning Python.",
    )

    user_memory.save_user_memory(
        user_id="user_123",
        memory="I am building an AI chatbot.",
    )

    memories = user_memory.get_user_memories("user_123")

    assert len(memories) == 2
    assert memories[0].memory == "I am learning Python."
    assert memories[1].memory == "I am building an AI chatbot."


def test_get_user_memories_only_returns_the_correct_user(
    test_session_factory,
    monkeypatch,
):
    monkeypatch.setattr(
        user_memory,
        "SessionLocal",
        test_session_factory,
    )

    user_memory.save_user_memory(
        user_id="user_123",
        memory="Memory belonging to user 123.",
    )

    user_memory.save_user_memory(
        user_id="user_456",
        memory="Memory belonging to user 456.",
    )

    memories = user_memory.get_user_memories("user_123")

    assert len(memories) == 1
    assert memories[0].user_id == "user_123"


def test_delete_user_memory(test_session_factory, monkeypatch):
    monkeypatch.setattr(
        user_memory,
        "SessionLocal",
        test_session_factory,
    )

    saved_memory = user_memory.save_user_memory(
        user_id="user_123",
        memory="This memory should be deleted.",
    )

    result = user_memory.delete_user_memory(
        memory_id=saved_memory.id,
        user_id="user_123",
    )

    assert result is True
    assert user_memory.get_user_memories("user_123") == []


def test_user_cannot_delete_another_users_memory(
    test_session_factory,
    monkeypatch,
):
    monkeypatch.setattr(
        user_memory,
        "SessionLocal",
        test_session_factory,
    )

    saved_memory = user_memory.save_user_memory(
        user_id="user_123",
        memory="This belongs to user 123.",
    )

    result = user_memory.delete_user_memory(
        memory_id=saved_memory.id,
        user_id="user_456",
    )

    assert result is False

    memories = user_memory.get_user_memories("user_123")

    assert len(memories) == 1
    assert memories[0].id == saved_memory.id


def test_delete_nonexistent_memory(test_session_factory, monkeypatch):
    monkeypatch.setattr(
        user_memory,
        "SessionLocal",
        test_session_factory,
    )

    result = user_memory.delete_user_memory(
        memory_id="nonexistent-id",
        user_id="user_123",
    )

    assert result is False