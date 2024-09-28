from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class PinCallbackData(CallbackData, prefix="pin"):
    data: str
    inline_message_id: str
