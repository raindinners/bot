from __future__ import annotations

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import PlayerCardsCallbackData


def player_cards_inline_keyboard_builder(inline_message_id: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Cards", callback_data=PlayerCardsCallbackData(inline_message_id=inline_message_id)
    )

    return builder
