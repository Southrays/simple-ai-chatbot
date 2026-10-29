from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_input: str = Field(
        min_length=1,
        max_length=4000,
        description="The message sent by the user",
    )
    conversation_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str | None = Field(description="The conversation id")
