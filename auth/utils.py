from datetime import datetime, timedelta
from enum import StrEnum

from fastapi import Response
from jose import JWTError, jwt

from auth.exceptions import InvalidTokenError
from auth.schemas import TokenInfo
from core.settings import AuthSettings


class TokenTypes(StrEnum):
    access = "access"
    pending_access = "pending_access"
    refresh = "refresh"
    verify = "verify"
    change_email = "change-email"


config = AuthSettings.get()


class TokenCreator:
    """Класс-генератор JWT токенов по user_id"""
    def __init__(self, user_id: int):
        self.user_id = user_id

    def _create_token(
            self,
            token_type: TokenTypes,
            age: timedelta
    ) -> str:
        expire = datetime.now() + age
        payload = {"sub": str(self.user_id), "exp": expire, "type": token_type}
        return jwt.encode(payload, config.secret_key, config.algorithm)

    @property
    def access(self) -> str:
        age = timedelta(minutes=config.access_token_expire_minutes)
        return self._create_token(TokenTypes.access, age)

    @property
    def verify(self) -> str:
        age = timedelta(hours=config.verify_token_expire_hours)
        return self._create_token(TokenTypes.verify, age)

    @property
    def pending_access(self) -> str:
        age = timedelta(hours=config.verify_token_expire_hours)
        return self._create_token(TokenTypes.pending_access, age)

    @property
    def refresh(self) -> str:
        age = timedelta(days=config.refresh_token_expire_days)
        return self._create_token(TokenTypes.refresh, age)

    @property
    def change_email(self) -> str:
        age = timedelta(hours=config.verify_token_expire_hours)
        return self._create_token(TokenTypes.change_email, age)


def decode_token(token: str) -> TokenInfo:
    """Декодирует JWT токен из SHA256"""
    try:
        payload = jwt.decode(
            token,
            config.secret_key,
            algorithms=[config.algorithm]
        )

        user_id = int(payload["sub"])
        token_type = payload["type"]

        return TokenInfo(user_id=user_id, type=token_type)
    except JWTError:
        raise InvalidTokenError("Невалидный или истекший токен")


from datetime import datetime, timedelta


def set_refresh_token_cookie(response: Response, token):
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        samesite="lax",  # или "strict" / "none" если фронтенд на другом домене
        max_age=60 * 60 * 24 * 7,  # 7 дней, или сколько нужно
        path="/"
    )


