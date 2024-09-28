from __future__ import annotations

import time
from contextlib import suppress
from typing import List, Tuple, Union

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from keyboards import (
    information_inline_keyboard_builder,
    player_cards_inline_keyboard_builder,
)
from logger import logger
from metadata import WINNERS_TIME
from poker import Poker


def get_response(poker: Poker) -> Union[List[Tuple[str, int]], List[int]]:
    return (
        [(str(result), stack) for result, stack in poker.engine.pot.pay(cards=poker.cards)]
        if poker.engine.positions.showdown
        else poker.engine.pot.pay_noshowdown()
    )


async def send_winners(bot: Bot, inline_message_id: str, poker: Poker) -> None:
    text: List[str] = list()  # noqa
    for index, chips in enumerate(get_response(poker=poker)):
        combination = None
        if isinstance(chips, Tuple):
            combination, chips = chips

        _player_id, player_name = poker.engine.players.players[index].id.split("_")

        text.append(
            f"Player: {player_name}, got - {combination.title() if combination else 'no combination'} and {chips} chips"
        )

    with suppress(TelegramBadRequest):
        await bot.edit_message_text(text="\n\n".join(text), inline_message_id=inline_message_id)
    with suppress(TelegramBadRequest):
        await bot.edit_message_reply_markup(
            inline_message_id=inline_message_id,
            reply_markup=player_cards_inline_keyboard_builder(inline_message_id=inline_message_id)
            .attach(information_inline_keyboard_builder(inline_message_id=inline_message_id))
            .as_markup(),
        )


async def winners(bot: Bot, inline_message_id: str, poker: Poker) -> None:
    if not poker.started or not poker.engine.round.terminal_state:
        return logger.debug("Skipping winners: wrong state")

    await send_winners(bot=bot, inline_message_id=inline_message_id, poker=poker)

    poker.started = False
    poker.winners_time = time.time() + WINNERS_TIME

    return None
