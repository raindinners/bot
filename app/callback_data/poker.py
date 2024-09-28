from __future__ import annotations

from typing import Literal

from aiogram.filters.callback_data import CallbackData


class PokerCallbackData(CallbackData, prefix="poker"):
    inline_message_id: str
    type: Literal["join", "exit"]
