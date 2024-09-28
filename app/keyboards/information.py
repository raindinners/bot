from __future__ import annotations

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import InformationCallbackData


def information_inline_keyboard_builder(inline_message_id: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Information",
        callback_data=InformationCallbackData(inline_message_id=inline_message_id),
    )

    return builder
