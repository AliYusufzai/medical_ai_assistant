from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from sqlalchemy.orm import DeclarativeBase

from app.core.config import config


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self) -> None:
        self.__engine: AsyncEngine = create_async_engine(
            config.DATABASE_URL, echo=config.DEBUG, pool_size=10, max_overflow=20
        )
        self.__session_factory = async_sessionmaker(
            self.__engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        return self.__engine
    
    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self.__session_factory
    
    async def close(self) -> None:
        await self.__engine.dispose()