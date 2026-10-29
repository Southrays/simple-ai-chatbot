#This is a version of the chabot.py with user-level
#Memory accross multiple conversations

from api_layer.monitoring.logger import logger
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver

from ai_layer.prompts.prompt import SYSTEM_PROMPT
from ai_layer.user_memory import get_user_memories, save_user_memory

#user_memory is setup, as seen above

load_dotenv()
checkpointer = InMemorySaver()

agent = create_agent(
    model="gpt-4o",
    tools=[],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

async def send_message(user_input: str, conversation_id: str, user_id: str) -> str:
    try:
        logger.debug("Invoking chat agent")

        #Memory implementation starts
        # Save a fact when the user explicitly asks us to remember it.
        prefix = "remember that "

        if user_input.lower().startswith(prefix):
            fact = user_input[len(prefix):].strip()
            if fact:
                save_user_memory(user_id, fact)

        # Retrieve this user's memories, regardless of conversation ID.
        memories = get_user_memories(user_id)

        memory_context = (
            "Known facts about this user:\n"
            + "\n".join(f"- {memory}" for memory in memories)
            if memories
            else "No saved facts about this user yet."
        )

        # Include user memory as context for the current turn.
        message = (
            f"{memory_context}\n\n"
            f"User's current message:\n{user_input}"
        )

        #Memory Implementation ends

        config: RunnableConfig = {"configurable": {"thread_id": conversation_id}}
        
        response = await agent.ainvoke(
            {"messages": [HumanMessage(content=message)]},
            config
        )

        logger.debug("Chat agent invocation successful")

        return response['messages'][-1].text
    
    except Exception:
        logger.exception("Chat agent invocation failed")
        raise

