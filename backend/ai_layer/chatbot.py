from api_layer.monitoring.logger import logger
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver

from ai_layer.prompts.prompt import SYSTEM_PROMPT

load_dotenv()
checkpointer = InMemorySaver()

agent = create_agent(
    model="gpt-4o",
    tools=[],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

async def send_message(user_input: str, conversation_id: str) -> str:
    try:
        logger.debug("Invoking chat agent")

        config: RunnableConfig = {"configurable": {"thread_id": conversation_id}}
        
        response = await agent.ainvoke(
            {"messages": [HumanMessage(content=user_input)]},
            config
        )

        logger.debug("Chat agent invocation successful")

        return response['messages'][-1].text
    
    except Exception:
        logger.exception("Chat agent invocation failed")
        raise

