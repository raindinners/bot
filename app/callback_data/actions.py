from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class ActionsCallbackData(CallbackData, prefix="actions"):
    is_done: bool = False
