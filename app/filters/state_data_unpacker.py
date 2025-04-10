from __future__ import annotations

from typing import Any, Dict, Union

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject


class StateDataUnpackerFilter(Filter):
    async def __call__(
        self, obj: TelegramObject, state: FSMContext
    ) -> Union[bool, Dict[str, Any]]:
        return {"state_data": await state.get_data()}
