from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.user.models import User
from app.modules.user.dto import UserCreate
from app.core.security import password_manager


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_by_id(self, user_id: str) -> User | None:
        result = await self.__db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.__db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.__db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate) -> User:

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=password_manager.hash(data.password),
        )
        self.__db.add(user)
        await self.__db.flush()  # sends INSERT to DB, but doesn't commit yet
        await self.__db.refresh(user)  # reloads user from DB (gets id, created_at)
        return user

    # async def update(self, user: User, data: UserUpdate) -> User:

    #     update_data = data.model_dump(exclude_unset=True)
    #     for field, value in update_data.items():
    #         setattr(
    #             user, field, value
    #         )  # setattr(obj, "bio", "hello") = obj.bio = "hello"

    #     self.__db.add(user)
    #     await self.__db.flush()
    #     await self.__db.refresh(user)
    #     return user

    async def email_exists(self, email: str) -> bool:
        return await self.get_by_email(email) is not None

    async def username_exists(self, username: str) -> bool:
        return await self.get_by_username(username) is not None
