from typing import AsyncGenerator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import database
from app.core.security import jwt_manager
from app.core.exceptions import AuthException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session_factory = database.get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt_manager.decode_token(token)
    except InvalidTokenError:
        raise AuthException.INVALID_CREDENTIALS

    if payload.get("type") != "access":
        raise AuthException.INVALID_CREDENTIALS

    user_id = payload.get("sub")
    if not user_id:
        raise AuthException.INVALID_CREDENTIALS

    # Import here to avoid circular imports
    from app.modules.user.service import UserService

    user_service = UserService(db)
    user = await user_service.get_by_id(str(user_id))

    if not user or not user.is_active:
        raise AuthException.INVALID_CREDENTIALS

    return user_id
