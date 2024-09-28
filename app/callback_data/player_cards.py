from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class PlayerCardsCallbackData(CallbackData, prefix="player_cards"):
    inline_message_id: str
