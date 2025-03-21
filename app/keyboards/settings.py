from __future__ import annotations

from typing import Any, Dict

from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.settings import server_settings


def settings_inline_keyboard_builder(values: Dict[str, Any]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Create", url=f"{server_settings.URL}?{server_settings.START_PARAMETER_NAME}={poker}"
    )

    return builder
