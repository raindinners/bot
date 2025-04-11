from __future__ import annotations

from typing import Optional

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User
from pokerengine.engine import EngineRake01
from redis.asyncio import Redis


class CurrentOrderFilter(Filter):
    async def __call__(
        self,
        obj: TelegramObject,
        event_from_user: Optional[User],
        state: FSMContext,
        redis: Redis,
        engine: EngineRake01,
    ) -> bool:
        if event_from_user is None:
            return False

        return event_from_user.id == int(engine.current_player.id)
