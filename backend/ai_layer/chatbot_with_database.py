#This is a version of the chabot.py with persistent database
#Memory accross multiple conversations
from typing import Any

from api_layer.monitoring.logger import logger

#From the database
from database.repositories.user_memory import get_user_memories, save_user_memory
from langchain.messages import HumanMessage
from langchain_core.runnables import RunnableConfig


async def send_message(
    agent: Any,
    user_input: str,
    conversation_id: str,
    user_id: str,
) -> str:
    try:
        logger.debug("Invoking database-backed chat agent")

        # Save explicitly requested user memories.
        prefix = "remember that "

        if user_input.lower().startswith(prefix):
            fact = user_input[len(prefix):].strip()

            if fact:
                save_user_memory(user_id, fact)

        # Retrieve persistent memories belonging to this user.
        memories = get_user_memories(user_id)

        memory_context = (
            "Known facts about this user:\n"
            + "\n".join(
                f"- {memory.memory}" for memory in memories
            )
            if memories
            else "No saved facts about this user yet."
        )

        # Include user memory in the current message.
        message = (
            f"{memory_context}\n\n"
            f"User's current message:\n{user_input}"
        )

        config: RunnableConfig = {
            "configurable": {
                "thread_id": conversation_id,
            }
        }

        response = await agent.ainvoke(
            {
                "messages": [
                    HumanMessage(content=message)
                ]
            },
            config=config,
        )

        logger.debug("Database-backed chat invocation successful")

        return response["messages"][-1].text

    except Exception:
        logger.exception("Database-backed chat invocation failed")
        raise

