from __future__ import annotations

from typing import Any, Dict, Union

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from redis.asyncio import Redis

from core.poker.schema import Poker


class PokerFilter(Filter):
    async def __call__(
        self,
        obj: TelegramObject,
        state: FSMContext,
        redis: Redis,
    ) -> Union[bool, Dict[str, Any]]:
        data = await state.get_data()
        if (poker := data.get("poker", None)) is None:
            return False

        poker = Poker.model_validate_json(await redis.get(name=poker))  # noqa
        return {
            "poker": poker,
            "engine": poker.engine.to_original(),
        }
