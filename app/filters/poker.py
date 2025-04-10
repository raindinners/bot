from __future__ import annotations

from typing import Any, Dict, Optional, Union

from aiogram.filters import CommandObject, Filter
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
        command: Optional[CommandObject] = None,
    ) -> Union[bool, Dict[str, Any]]:
        data = await state.get_data()

        name = data.get("poker", None)
        if command and command.args:
            name = command.args
        if name is None:
            return False

        poker = Poker.model_validate_json(await redis.get(name=name))
        return {
            "poker": poker,
            "engine": poker.engine.to_original(),
        }
