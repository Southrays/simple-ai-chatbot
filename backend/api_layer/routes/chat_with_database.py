#This is a version of the chat.py with persistent database
#Memory accross multiple conversations

from uuid import uuid4

from ai_layer.chatbot_with_database import send_message
from fastapi import APIRouter, HTTPException, Request

from api_layer.monitoring.logger import logger
from api_layer.schemas.chat_with_user_level_memory import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat_with_database", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: Request, chat_request: ChatRequest) -> ChatResponse:
    try:
        logger.info("Database-backed chat request received")

        conversation_id = (
            chat_request.conversation_id or str(uuid4())
        )

        agent = request.app.state.agent

        answer = await send_message(
            agent=agent,
            user_input=chat_request.user_input,
            conversation_id=conversation_id,
            user_id=chat_request.user_id,
        )

        logger.info("Database-backed chat request completed")

        return ChatResponse(
            response=answer,
            conversation_id=conversation_id,
        )

    except (ValueError, KeyError, RuntimeError):
        logger.exception("Database-backed chat request failed")

        raise HTTPException(
            status_code=502,
            detail="The AI service could not complete your request.",
        ) from None