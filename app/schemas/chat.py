from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from app.models.message import MessageRole

class MessageSend(BaseModel):
    message: str = Field(..., min_lenght=1, max_length=5000)
    conversation_Id: int | None = None

class MessageResponse(BaseModel):
    id: int
    role: MessageRole
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ConversationWithMessages(ConversationResponse):
    messages: List[MessageResponse]

class ChatResponse(BaseModel):
    conversation_id: int
    user_message: str
    ai_response: str