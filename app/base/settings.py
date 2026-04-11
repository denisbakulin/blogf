from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

env_dir = Path(__file__).parent.parent.parent / "envs"


class ModeSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_dir / ".env.mode", extra="ignore")
    MODE: Literal["DEV", "PROD"] = "DEV"


mode = ModeSettings()
current_env_file = env_dir / (".env.prod" if mode.MODE == "PROD" else ".env.dev")




class JWTAuthSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    tg_login_token_expire_minutes: int
    refresh_token_expire_days: int


class GoogleOAuthSettings(BaseSettings):
    client_secret: str
    client_id: str


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379


class TgBotSettings(BaseSettings):
    token: str
    name: str


class AdminSettings(BaseSettings):
    login: str
    password: str


class Settings(BaseSettings):
    jwt: JWTAuthSettings
    google: GoogleOAuthSettings
    redis: RedisSettings
    admin: AdminSettings

    bot: TgBotSettings

    model_config = SettingsConfigDict(
        env_file=current_env_file,
        env_nested_delimiter="__",
        extra="ignore"
    )


settings = Settings()

print(f"settings was loaded by file: {current_env_file.name}")


