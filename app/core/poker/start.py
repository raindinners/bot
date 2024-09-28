from __future__ import annotations

import math
import random
import time
from contextlib import suppress
from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from pokerengine.constants import MAX_PLAYERS, MIN_PLAYERS

from enums import GameState
from keyboards import poker_inline_keyboard_builder
from logger import logger
from metadata import RANDOM_MAX_VALUE, RANDOM_MIN_VALUE, START_TIME
from poker import Poker
from schemas import ApplicationSchema


class StartResponse(ApplicationSchema):
    state: GameState
    time: Optional[float] = None


def is_ready_to_start(poker: Poker) -> bool:
    players_to_save = [
        player for player in poker.engine.players.players if player.stack and not player.is_left
    ]
    poker.engine.players.set_players(players=players_to_save)

    return MIN_PLAYERS <= len(poker.engine.players.players) <= MAX_PLAYERS


async def send_start_message(
    bot: Bot,
    inline_message_id: str,
    state: GameState,
    time_: float,
) -> None:
    match state:
        case GameState.STARTING:
            text = f"The game will start in {math.ceil(time_ - time.time())} seconds!"
        case GameState.STARTED:
            text = "The game was started!"
        case _:
            text = "The game was stopped."

    with suppress(TelegramBadRequest):
        await bot.edit_message_text(text=text, inline_message_id=inline_message_id)

    with suppress(TelegramBadRequest):
        await bot.edit_message_reply_markup(
            inline_message_id=inline_message_id,
            reply_markup=poker_inline_keyboard_builder(
                inline_message_id=inline_message_id
            ).as_markup(),
        )


async def start(bot: Bot, inline_message_id: str, poker: Poker) -> None:
    if poker.started:
        return logger.debug("Skipping start: wrong state")

    if poker.winners_time and time.time() < poker.winners_time:
        return logger.debug("Skipping start: wrong state")

    if not is_ready_to_start(poker=poker):
        if poker.start_at or poker.winners_time:
            await send_start_message(
                bot=bot,
                inline_message_id=inline_message_id,
                state=GameState.STOPPED,
                time_=poker.start_at,
            )
            poker.seed = random.randint(RANDOM_MIN_VALUE, RANDOM_MAX_VALUE)

        poker.stop()
        return logger.debug("Skipping start: wrong state")

    if not poker.start_at:
        poker.start_at = time.time() + START_TIME
        await send_start_message(
            bot=bot,
            inline_message_id=inline_message_id,
            state=GameState.STARTING,
            time_=poker.start_at,
        )

    if time.time() < poker.start_at:
        return logger.debug("Skipping start game: wrong time")

    poker.start()
    await send_start_message(
        bot=bot, inline_message_id=inline_message_id, state=GameState.STARTED, time_=poker.start_at
    )

    return None
