
from uuid import uuid4

from sqlalchemy import select

from database.connection import SessionLocal
from database.models import UserMemory


def save_user_memory(
    user_id: str,
    memory: str,
) -> UserMemory:
    with SessionLocal() as session:
        user_memory = UserMemory(
            id=str(uuid4()),
            user_id=user_id,
            memory=memory,
        )

        session.add(user_memory)
        session.commit()
        session.refresh(user_memory)

        return user_memory


def get_user_memories(
    user_id: str,
) -> list[UserMemory]:
    with SessionLocal() as session:
        statement = (
            select(UserMemory)
            .where(UserMemory.user_id == user_id)
            .order_by(UserMemory.created_at)
        )

        memories = list(session.scalars(statement).all())

        return memories


def delete_user_memory(
    memory_id: str,
    user_id: str,
) -> bool:
    with SessionLocal() as session:
        statement = (
            select(UserMemory)
            .where(
                UserMemory.id == memory_id,
                UserMemory.user_id == user_id,
            )
        )

        memory = session.scalar(statement)

        if memory is None:
            return False

        session.delete(memory)
        session.commit()

        return True
