from __future__ import annotations

from dotenv import load_dotenv
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

load_dotenv()


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
