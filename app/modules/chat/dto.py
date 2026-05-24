from datetime import datetime
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=5, description="Question to ask the medical AI")


class AskResponse(BaseModel):
    conversation_id: int
    question: str
    answer: str
    sources: list[str]


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}