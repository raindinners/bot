from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.event.bases import CancelHandler, SkipHandler
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from pokerengine.schema import EngineRake01


class PokerAutoSaverMiddleware(BaseMiddleware):
    def __init__(
        self, poker_key: str = "poker", engine_key: str = "engine", redis_key: str = "redis"
    ) -> None:
        self.poker_key = poker_key
        self.engine_key = engine_key
        self.redis_key = redis_key

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            result = await handler(event, data)
        except (SkipHandler, CancelHandler):
            raise

        if (
            (poker := data.get(self.poker_key, None)) is not None
            and (engine := data.get(self.engine_key, None)) is not None
            and (redis := data.get(self.redis_key, None)) is not None
        ):
            poker.engine = EngineRake01.from_original(value=engine)  # noqa
            await redis.set(name=poker.id, value=poker.model_dump_json())  # noqa

        return result
