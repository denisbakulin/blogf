from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

path_dir = Path(__file__).parent.parent.parent


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=path_dir / ".env",
        extra="ignore"
    )


class JWTAuthSettings(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix="JWT_"
    )

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


class SuperAdminSettings(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix="SUPER_ADMIN_"
    )

    username: str
    password: str


class AnonUserSettings(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix="ANON_"
    )

    username: str
    password: str


class TgBotSettings(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix="TG_BOT_"
    )

    token: str
    secret: str


jwt_auth_settings = JWTAuthSettings()
super_admin_settings = SuperAdminSettings()
anon_settings = AnonUserSettings()
tg_bot_settings = TgBotSettings()