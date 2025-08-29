from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import EmailStr



class BaseConfig(BaseSettings):

    class Config:
        env_file = ".env"
        extra = "ignore"

class AppConfig(BaseConfig):

    app_name: str
    db_uri: str




class AuthConfig(BaseConfig):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    verify_token_expire_hours: int


class MailConfig(BaseConfig):
    mail_username: EmailStr
    mail_password: str
    mail_from: EmailStr
    mail_port: int = 587
    mail_server: str = "smtp.yandex.ru"
    mail_from_name: str = "blogf"
    mail_tls: bool = True
    mail_ssl: bool = False



@lru_cache
def get_app_config() -> AppConfig:
    return AppConfig()

@lru_cache
def get_auth_config() -> AuthConfig:
    return AuthConfig()

@lru_cache
def get_mail_config() -> MailConfig:
    return MailConfig()

