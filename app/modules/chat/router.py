from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.modules.chat.service import ChatService
from app.modules.chat.dto import (
    AskRequest,
    AskResponse,
    ConversationResponse,
    MessageResponse,
)
from app.modules.user.models import User

router = APIRouter()


@router.post("/conversations", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    data: AskRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return await service.create_conversation(current_user.id, title=data.question)


@router.get("/conversations", response_model=list[ConversationResponse])
async def get_conversations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return await service.get_conversations(current_user.id)


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
async def get_messages(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return await service.get_messages(conversation_id, current_user.id)


@router.post("/conversations/{conversation_id}/ask", response_model=AskResponse)
async def ask(
    conversation_id: int,
    data: AskRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return await service.ask(conversation_id, data.question, current_user.id)