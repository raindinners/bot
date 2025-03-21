from __future__ import annotations

from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.settings import server_settings


def create_inline_keyboard_builder(poker: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Create", url=f"{server_settings.URL}?{server_settings.START_PARAMETER_NAME}={poker}"
    )

    return builder
