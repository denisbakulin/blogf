from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


__all__ = (
    "bot_settings"
)

env_path = Path(__file__).parent


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path / ".env",
        extra="ignore"
    )

class TgBotSettings(BaseConfig):
    token: str


bot_settings = TgBotSettings()
