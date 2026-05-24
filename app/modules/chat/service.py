from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import ollama

from app.core.config import config
from app.core.exceptions import ChatException
from app.modules.chat.models import Conversation, Message
from app.modules.chat.dto import AskResponse
from app.core.exceptions import ChatException


class ChatService:
    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def create_conversation(self, user_id: int, title: str) -> Conversation:
        conversation = Conversation(user_id=user_id, title=title)
        self.__db.add(conversation)
        await self.__db.flush()
        await self.__db.refresh(conversation)
        return conversation

    async def get_conversations(self, user_id: int) -> list[Conversation]:
        result = await self.__db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_messages(self, conversation_id: int, user_id: int) -> list[Message]:
        conversation = await self.__get_conversation(conversation_id, user_id)
        if not conversation:
            raise ChatException.NOT_FOUND

        result = await self.__db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return list(result.scalars().all())

    async def ask(self, conversation_id: int, question: str, user_id: int) -> AskResponse:
        conversation = await self.__get_conversation(conversation_id, user_id)
        if not conversation:
            raise ChatException.NOT_FOUND

        recent_messages = await self.__get_recent_messages(conversation_id)

        from app.rag.pipeline import pipeline
        chunks = await pipeline.search(question, user_id)
        if not chunks:
            raise ChatException.NO_DOCUMENTS

        context = "\n\n".join(chunks)
        history = "\n".join([f"{m.role}: {m.content}" for m in recent_messages])

        prompt = f"""You are a medical AI assistant. Use the following medical document context to answer the question accurately.

MEDICAL CONTEXT:
{context}

CONVERSATION HISTORY:
{history}

USER QUESTION:
{question}

Provide a clear, accurate medical response based on the context provided. If the answer is not in the context, say so clearly."""

        response = await ollama.AsyncClient(host=config.OLLAMA_URL).chat(
            model=config.OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.message.content or "I could not generate a response."

        self.__db.add(Message(conversation_id=conversation_id, role="user", content=question))
        self.__db.add(Message(conversation_id=conversation_id, role="assistant", content=answer))
        await self.__db.flush()

        return AskResponse(
            conversation_id=conversation_id,
            question=question,
            answer=answer,
            sources=chunks,
        )

    async def __get_conversation(self, conversation_id: int, user_id: int) -> Conversation | None:
        result = await self.__db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def __get_recent_messages(self, conversation_id: int, limit: int = 10) -> list[Message]:
        result = await self.__db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        return list(reversed(result.scalars().all()))