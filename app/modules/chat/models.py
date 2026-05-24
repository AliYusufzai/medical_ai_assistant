from sqlalchemy import ForeignKey, String, Text, text, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Conversation(Base):
    __tablename__ = 'conversations'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    

class Message(Base):
    __tablename__ = 'messages'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey('conversations.id'), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), nullable=False)