import secrets
import string
from datetime import datetime, timedelta
from enum import StrEnum

from base.settings import jwt_auth_settings
from exceptions.auth import InvalidTokenError
from fastapi import Response
from jose import JWTError, jwt
from schemas.auth import TokenInfo

def generate_auth_code() -> str:
    """
    XkP_1_v8QJzS8V9_Z_5v8QJzS8V9_Z_5v8QJzS8V9_Z
    """

    return secrets.token_urlsafe(32)


def check_password(password):
    """
    Простая проверка пароля:
    - Минимум 8 символов
    - Хотя бы одна цифра
    - Хотя бы одна заглавная буква
    - Хотя бы одна строчная буква
    """

    if len(password) < 8:
        return False, "Пароль должен содержать минимум 8 символов"

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    if not has_upper:
        return False, "Пароль должен содержать хотя бы одну заглавную букву"
    if not has_lower:
        return False, "Пароль должен содержать хотя бы одну строчную букву"
    if not has_digit:
        return False, "Пароль должен содержать хотя бы одну цифру"

    return True, "Пароль надежный"



class TokenTypes(StrEnum):
    access = "access"
    refresh = "refresh"


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
        return jwt.encode(payload, jwt_auth_settings.secret_key, jwt_auth_settings.algorithm)

    @property
    def access(self) -> str:
        age = timedelta(minutes=jwt_auth_settings.access_token_expire_minutes)
        return self._create_token(TokenTypes.access, age)

    @property
    def refresh(self) -> str:
        age = timedelta(days=jwt_auth_settings.refresh_token_expire_days)
        return self._create_token(TokenTypes.refresh, age)



def decode_token(token: str) -> TokenInfo:
    """Декодирует JWT токен из SHA256"""

    try:
        payload = jwt.decode(
            token,
            jwt_auth_settings.secret_key,
            algorithms=[jwt_auth_settings.algorithm]
        )

        user_id = int(payload["sub"])
        token_type = payload["type"]

        return TokenInfo(user_id=user_id, type=token_type)
    except JWTError:
        raise InvalidTokenError("Невалидный или истекший токен")


def set_refresh_token_cookie(response: Response, token):
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
        path="/"
    )



