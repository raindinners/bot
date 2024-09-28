from __future__ import annotations

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import CreateCallbackData
from enums import Games


def create_inline_keyboard_builder(game: Games) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Create", callback_data=CreateCallbackData(game=game.name))

    return builder
