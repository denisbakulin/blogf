from datetime import datetime, timedelta
from jose import jwt, JWTError
from core.config import AuthConfig
from auth.schemas import TokenInfo
from auth.exceptions import InvalidTokenErr
from fastapi import Response
from enum import StrEnum


class TokenTypes(StrEnum):
    access = "access"
    refresh = "refresh"
    verify = "verify"
    change_email = "change-email"


config = AuthConfig.get()


class TokenCreator:

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
    def refresh(self) -> str:
        age = timedelta(days=config.refresh_token_expire_days)
        return self._create_token(TokenTypes.refresh, age)

    @property
    def change_email(self) -> str:
        age = timedelta(hours=config.verify_token_expire_hours)
        return self._create_token(TokenTypes.change_email, age)


def decode_token(token: str) -> TokenInfo | None:
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
        raise InvalidTokenErr("Invalid token or expired")


def set_refresh_token_cookie(response: Response, token):
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/auth/refresh",
        max_age=config.refresh_token_expire_days*3600*24,

    )


