from __future__ import annotations

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class LoggingSettings(BaseSettings):
    MAIN_LOGGER_NAME: str
    LOGGING_LEVEL: str


logging_settings = LoggingSettings()


class BotSettings(BaseSettings):
    BOT_TOKEN: str


bot_settings = BotSettings()


class ServerSettings(BaseSettings):
    URL: str = "https://localhost:5173"
    START_PARAMETER_NAME: str = "startapp"


server_settings = ServerSettings()
