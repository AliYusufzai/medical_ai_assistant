from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user.models import User
from app.modules.user.dto import UserCreate, UserResponse
from app.modules.user.service import UserService
from app.modules.auth.dto import LoginRequest, TokenResponse
from app.core.security import password_manager, jwt_manager
from app.core.exceptions import AuthException, UserException


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.__db = db
        # OOP CONCEPT: Composition — AuthService owns a UserService instance
        self.__user_service = UserService(db)


    async def register(self, data: UserCreate) -> TokenResponse:

        # Step 1 — check email uniqueness
        if await self.__user_service.email_exists(data.email):
            raise UserException.EMAIL_TAKEN

        # Step 2 — check username uniqueness
        if await self.__user_service.username_exists(data.username):
            raise UserException.USERNAME_TAKEN

        # Step 3 — create user (password hashing happens inside UserService)
        user = await self.__user_service.create(data)

        # Step 4 — generate tokens and return
        return self.__generate_tokens(user)
    

    async def login(self, data: LoginRequest) -> TokenResponse:

        # Step 1 — find user
        user = await self.__user_service.get_by_email(data.email)
        if not user:
            raise AuthException.INVALID_CREDENTIALS

        # Step 2 — verify password
        if not password_manager.verify(data.password, user.hashed_password):
            raise AuthException.INVALID_CREDENTIALS

        # Step 3 — check account is active
        if not user.is_active:
            raise AuthException.ACCOUNT_DEACTIVATED

        # Step 4 — return tokens
        return self.__generate_tokens(user)
    

    async def refresh(self, refresh_token: str) -> TokenResponse:

        try:
            payload = jwt_manager.decode_token(refresh_token)
        except InvalidTokenError:
            raise AuthException.INVALID_REFRESH_TOKEN

        # Make sure client didn't send an access token by mistake
        if payload.get("type") != "refresh":
            raise AuthException.INVALID_TOKEN_TYPE

        user_id = payload.get("sub")
        if not user_id:
            raise AuthException.INVALID_TOKEN_PAYLOAD

        user = await self.__user_service.get_by_id(str(user_id))
        if not user or not user.is_active:
            raise AuthException.ACCOUNT_DEACTIVATED

        return self.__generate_tokens(user)
    

    def __generate_tokens(self, user: User) -> TokenResponse:
        token_data = {"sub": str(user.id)}

        return TokenResponse(
            access_token=jwt_manager.create_access_token(token_data),
            refresh_token=jwt_manager.create_refresh_token(token_data),
            user=UserResponse.model_validate(user),
        )