from __future__ import annotations

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import PinCallbackData


def pin_inline_keyboard_builder(inline_message_id: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="1",
            callback_data=PinCallbackData(data="1", inline_message_id=inline_message_id).pack(),
        ),
        InlineKeyboardButton(
            text="2",
            callback_data=PinCallbackData(data="2", inline_message_id=inline_message_id).pack(),
        ),
        InlineKeyboardButton(
            text="3",
            callback_data=PinCallbackData(data="3", inline_message_id=inline_message_id).pack(),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="4",
            callback_data=PinCallbackData(data="4", inline_message_id=inline_message_id).pack(),
        ),
        InlineKeyboardButton(
            text="5",
            callback_data=PinCallbackData(data="5", inline_message_id=inline_message_id).pack(),
        ),
        InlineKeyboardButton(
            text="6",
            callback_data=PinCallbackData(data="6", inline_message_id=inline_message_id).pack(),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="7",
            callback_data=PinCallbackData(data="7", inline_message_id=inline_message_id).pack(),
        ),
        InlineKeyboardButton(
            text="8",
            callback_data=PinCallbackData(data="8", inline_message_id=inline_message_id).pack(),
        ),
        InlineKeyboardButton(
            text="9",
            callback_data=PinCallbackData(data="9", inline_message_id=inline_message_id).pack(),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="C",
            callback_data=PinCallbackData(data="C", inline_message_id=inline_message_id).pack(),
        ),
        InlineKeyboardButton(
            text="0",
            callback_data=PinCallbackData(data="0", inline_message_id=inline_message_id).pack(),
        ),
        InlineKeyboardButton(
            text="<",
            callback_data=PinCallbackData(data="<", inline_message_id=inline_message_id).pack(),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="<<",
            callback_data=PinCallbackData(data="<<", inline_message_id=inline_message_id).pack(),
        ),
        InlineKeyboardButton(
            text="=",
            callback_data=PinCallbackData(data="=", inline_message_id=inline_message_id).pack(),
        ),
        InlineKeyboardButton(
            text=">>",
            callback_data=PinCallbackData(data=">>", inline_message_id=inline_message_id).pack(),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=" ",
            callback_data=PinCallbackData(data="no", inline_message_id=inline_message_id).pack(),
        ),
        InlineKeyboardButton(
            text="Amount",
            callback_data=PinCallbackData(
                data="amount", inline_message_id=inline_message_id
            ).pack(),
        ),
        InlineKeyboardButton(
            text=" ",
            callback_data=PinCallbackData(data="no", inline_message_id=inline_message_id).pack(),
        ),
    )
    return builder
