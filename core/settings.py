from functools import lru_cache
from typing import Self

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):

    @classmethod
    @lru_cache
    def get(cls) -> Self:
        return cls()

    class Config:
        env_file = ".env"
        extra = "ignore"


class AppSettings(BaseConfig):
    app_name: str
    db_uri: str


class AuthSettings(BaseConfig):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    verify_token_expire_hours: int

    class Config(BaseConfig.Config):
        env_prefix = "JWT_"

class MailSettings(BaseConfig):
    username: EmailStr
    password: str
    port: int
    server: str
    tls: bool = True
    ssl: bool = False

    class Config(BaseConfig.Config):
        env_prefix = "MAIL_"


class FirstAdminSettings(BaseConfig):
    username: str
    password: str
    email: EmailStr

    class Config(BaseConfig.Config):
        env_prefix = "FIRST_ADMIN_"

