from datetime import datetime, timedelta
from jose import jwt, JWTError
from core.config import get_auth_config
from auth.schemas import TokenInfo
from auth.exceptions import InvalidTokenErr
from fastapi import Response
from typing import Literal


token_types = Literal["access", "refresh", "verify"]


config = get_auth_config()


def create_token(
    token_type: token_types,
    user_id: int,
    age: timedelta
) -> str:
    expire = datetime.now() + age
    payload = {"sub": str(user_id), "exp": expire, "type": token_type}
    return jwt.encode(payload, config.secret_key, config.algorithm)


def create_access_token(user_id: int) -> str:
    age = timedelta(minutes=config.access_token_expire_minutes)
    return create_token("access", user_id, age)

def create_verify_token(user_id: int) -> str:
    age = timedelta(hours=config.verify_token_expire_hours)
    return create_token("verify", user_id, age)


def create_refresh_token(user_id: int) -> str:
    age = timedelta(days=config.refresh_token_expire_days)
    return create_token("refresh", user_id, age)


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

