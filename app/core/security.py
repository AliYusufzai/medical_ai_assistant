from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from app.core.config import config


class PasswordManager:
    def __init__(self) -> None:
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self.__pwd_context.hash(password)

    def verify(self, plain: str, hashed: str) -> bool:
        return self.__pwd_context.verify(plain, hashed)


class JWTManager:
    def __init__(self) -> None:
        self.__secret_key = config.JWT_SECRET_KEY
        self.__algorithm = config.JWT_ALGORITHM

    def __create_token(self, payload: dict[str, Any], expires_delta: timedelta) -> str:
        expire = datetime.now(timezone.utc) + expires_delta
        payload.update({"exp": expire})
        return jwt.encode(payload, self.__secret_key, algorithm=self.__algorithm)

    def create_access_token(self, data: dict[str, Any]) -> str:
        return self.__create_token(
            payload={**data, "type": "access"},
            expires_delta=timedelta(minutes=config.JWT_ACCESS_EXPIRE_MINUTES),
        )

    def create_refresh_token(self, data: dict[str, Any]) -> str:
        return self.__create_token(
            payload={**data, "type": "refresh"},
            expires_delta=timedelta(days=config.JWT_REFRESH_EXPIRE_DAYS),
        )

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
        except InvalidTokenError:
            raise


password_manager = PasswordManager()
jwt_manager = JWTManager()
