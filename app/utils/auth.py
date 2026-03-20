import secrets
from datetime import UTC, datetime, timedelta
from enum import StrEnum

from base.settings import jwt_auth_settings
from exceptions.auth import InvalidPasswordError, InvalidTokenError
from fastapi import Response
from jose import JWTError, jwt
from passlib.context import CryptContext
from schemas.auth import LoginTokens, TokenInfo

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def verify_password(password, hashed_password) -> bool:
    return pwd_context.verify(password, hashed_password)



def generate_hashed_password(password) -> str:
    password_bytes = password.encode('utf-8')

    # Если пароль длиннее 72 байтов - обрезаем его
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode('utf-8', 'ignore')

    return pwd_context.hash(password)


def generate_auth_code() -> str:
    """
    XkP_1_v8QJzS8V9_Z_5v8QJzS8V9_Z_5v8QJzS8V9_Z
    """

    return secrets.token_urlsafe(32)


def check_password(password) -> tuple[bool, str]:

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
    tg_login = "tg_login"



class TokenCreator:
    """Класс-генератор JWT токенов по author_id"""
    def __init__(self, user_id: int):
        self.user_id = user_id

    def _create_token(
            self,
            token_type: TokenTypes,
            age: timedelta
    ) -> str:
        # 1. Берем текущее время в UTC
        now = datetime.now(UTC)
        # 2. Вычисляем время истечения и превращаем в число (timestamp)
        expire = int((now + age).timestamp())

        payload = {
            "sub": str(self.user_id),
            "exp": expire,
            "type": token_type
        }

        return jwt.encode(
            payload,
            jwt_auth_settings.secret_key,
            algorithm=jwt_auth_settings.algorithm
        )

    @property
    def access(self) -> str:
        age = timedelta(minutes=jwt_auth_settings.access_token_expire_minutes)
        return self._create_token(TokenTypes.access, age)

    @property
    def refresh(self) -> str:
        age = timedelta(days=jwt_auth_settings.refresh_token_expire_days)
        return self._create_token(TokenTypes.refresh, age)

    @property
    def tg_login(self) -> str:
        age = timedelta(minutes=jwt_auth_settings.tg_login_token_expire_minutes)
        return self._create_token(TokenTypes.tg_login, age)



    @property
    def auth_tokens(self) -> LoginTokens:
        tokens = type(self)(self.user_id)

        return LoginTokens(
            access=tokens.access,
            refresh=tokens.refresh
        )


def decode_token(token: str, algorithm: str | None = None):
    try:
        return jwt.decode(
            token,
            jwt_auth_settings.secret_key,
            algorithms=[algorithm or jwt_auth_settings.algorithm],
            options={
                "verify_signature": True,
                "verify_exp": True,
            }
        )

    except JWTError as e:
        raise InvalidTokenError("Невалидный или истекший токен") from e

def get_decoded_token(token: str) -> TokenInfo:
    """Декодирует JWT токен из SHA256"""

    payload = decode_token(token)
    user_id = int(payload["sub"])
    token_type = payload["type"]

    return TokenInfo(user_id=user_id, type=token_type)

def ensure_correct_password(pwd: str):
    is_pwd_correct, msg = check_password(pwd)
    if not is_pwd_correct:
        raise InvalidPasswordError(msg)





def set_refresh_token_cookie(response: Response, token):
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
        path="/"
    )



