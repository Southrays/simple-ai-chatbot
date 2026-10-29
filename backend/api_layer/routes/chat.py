from uuid import uuid4

from ai_layer.chatbot import send_message
from fastapi import APIRouter, HTTPException

from api_layer.monitoring.logger import logger
from api_layer.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        logger.info("Chat request received")

        conversation_id = request.conversation_id or str(uuid4())

        answer = await send_message(request.user_input, conversation_id)

        logger.info("Chat request completed successfully")

        return ChatResponse(response=answer, conversation_id=conversation_id)

    except (ValueError, KeyError):
        logger.exception("Chat request failed")

        raise HTTPException(
            status_code=502,
            detail="The AI service could not complete your request.",
        ) from None