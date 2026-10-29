from collections import defaultdict

# Temporary memory shared across conversations.
# All data is lost when the backend process restarts.
_user_memories: dict[str, list[str]] = defaultdict(list)

def get_user_memories(user_id: str) -> list[str]:
    """Retrieve saved memories for a user."""
    return _user_memories[user_id]


def save_user_memory(user_id: str, memory: str) -> None:
    """Save a new memory for a user."""
    memory = memory.strip()

    if memory and memory not in _user_memories[user_id]:
        _user_memories[user_id].append(memory)