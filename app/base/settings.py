from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_dir = Path(__file__).parent.parent.parent / "envs"


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_dir / ".env.backend",
        extra="ignore"
    )


class JWTAuthSettings(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix="JWT_"
    )

    secret_key: str
    algorithm: str

    access_token_expire_minutes: int
    tg_login_token_expire_minutes: int
    refresh_token_expire_days: int


class GoogleOAuthSettings(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix="GOOGLE_OAUTH_"
    )

    client_secret: str
    client_id: str


class TgBotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_dir / ".env.bot",
        extra="ignore"
    )

    token: str
    bot_name: str


bot_settings = TgBotSettings()
jwt_auth_settings = JWTAuthSettings()
google_oauth_settings = GoogleOAuthSettings()
