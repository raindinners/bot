from __future__ import annotations

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import PokerCallbackData


def poker_inline_keyboard_builder(inline_message_id: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Join",
        callback_data=PokerCallbackData(inline_message_id=inline_message_id, type="join").pack(),
    )
    builder.button(
        text="Exit",
        callback_data=PokerCallbackData(inline_message_id=inline_message_id, type="exit").pack(),
    )

    return builder
