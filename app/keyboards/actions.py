from __future__ import annotations

from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data.action import ActionCallbackData
from enums import Action as ActionE
from schemas import Action


def actions_inline_keyboard_builder(
    inline_message_id: str, actions: List[Action]
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for action in actions:
        builder.button(
            text=f"{ActionE(action.action).as_string()}: {action.amount}",
            callback_data=ActionCallbackData(
                inline_message_id=inline_message_id,
                action=action.action,
            ).pack(),
        )

    return builder
