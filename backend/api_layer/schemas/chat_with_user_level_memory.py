#This is a version of the chat.py with user-level
#Memory accross multiple conversations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_input: str = Field(
        min_length=1,
        max_length=4000,
        description="The message sent by the user",
    )
    conversation_id: str | None = None
    user_id: str = "demo-user" #It only adds user_id to the request

class ChatResponse(BaseModel):
    response: str
    conversation_id: str | None = Field(description="The conversation id")
