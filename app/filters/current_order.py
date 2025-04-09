from __future__ import annotations

from typing import Optional

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User
from pokerengine.engine import EngineRake01
from redis.asyncio import Redis

from utils.id import get_player_id


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

        return get_player_id(user=event_from_user) == engine.current_player.id
