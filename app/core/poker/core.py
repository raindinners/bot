from __future__ import annotations

import random
import time
from contextlib import suppress

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from pokerengine.constants import MAX_PLAYERS, MIN_PLAYERS
from pokerengine.engine import Player
from pokerengine.schema import EngineRake01
from redis.asyncio import Redis

from logger import logger
from messages import (
    send_loading_state_message_broadcast,
    send_main_state_message,
    send_winners_message_broadcast,
)
from metadata import (
    POKER_START_TIME,
    POKER_WINNERS_TIME,
    RANDOM_MAX_VALUE,
    RANDOM_MIN_VALUE,
)
from states import States

from .schema import Poker


async def poker_main_job_core(bot: Bot, poker: Poker) -> None:
    await start(bot=bot, poker=poker)
    await winners(bot=bot, poker=poker)


async def poker_main_job(bot: Bot, poker: Poker, redis: Redis) -> None:
    _poker = Poker.model_validate_json(await redis.get(name=poker.id))

    try:
        await poker_main_job_core(bot=bot, poker=_poker)
    except Exception as exc:
        logger.exception(exc)

    await redis.set(name=poker.id, value=_poker.model_dump_json())


async def poker_chat_job_core(bot: Bot, poker: Poker, player: Player, state: FSMContext) -> None:
    await poker_chat_updater(bot=bot, poker=poker, player=player, state=state)


async def poker_chat_job(
    bot: Bot, poker: Poker, player: Player, state: FSMContext, redis: Redis
) -> None:
    _poker = Poker.model_validate_json(await redis.get(name=poker.id))

    try:
        await poker_chat_job_core(bot=bot, poker=_poker, player=player, state=state)
    except Exception as exc:
        logger.exception(exc)

    await redis.set(name=poker.id, value=_poker.model_dump_json())


async def start(bot: Bot, poker: Poker) -> None:
    if poker.started:
        logger.debug("Skipping start: wrong state")
        return

    if poker.winners_time and time.time() < poker.winners_time:
        logger.debug("Skipping start: wrong state")
        return

    if not (MIN_PLAYERS <= len(poker.engine.players) <= MAX_PLAYERS):
        if poker.start_at or poker.winners_time:
            await send_loading_state_message_broadcast(
                bot=bot, players=poker.engine.players, is_stopped=True
            )

        poker.stop()

        logger.debug("Skipping start: wrong state")
        return

    if not poker.start_at:
        poker.start_at = time.time() + POKER_START_TIME
        await send_loading_state_message_broadcast(
            bot=bot, players=poker.engine.players, start_at=poker.start_at
        )

    if time.time() < poker.start_at:
        logger.debug("Skipping start game: wrong time")
        return

    poker.engine.players = [player for player in poker.engine.players if player.stack]
    poker.seed = random.randint(RANDOM_MIN_VALUE, RANDOM_MAX_VALUE)
    poker.start()


async def winners(bot: Bot, poker: Poker) -> None:
    engine = poker.engine.to_original()
    if not poker.started or not engine.showdown:
        logger.debug("Skipping winners: wrong state")
        return

    with suppress(Exception):
        await send_winners_message_broadcast(
            bot=bot,
            poker=poker,
            response=(
                [(str(result), stack) for result, stack in engine.pay(cards=poker.cards)]
                if engine.terminal_state
                else engine.pay_noshowdown()
            ),
        )
    poker.engine = EngineRake01.from_original(value=engine)
    poker.winners_time = time.time() + POKER_WINNERS_TIME


async def poker_chat_updater(bot: Bot, poker: Poker, player: Player, state: FSMContext) -> None:
    engine = poker.engine.to_original()
    if not poker.started or engine.showdown:
        player.parameters = {**player.parameters, "last_round": None, "last_player_id": None}
        return

    current_state = await state.get_state()
    if current_state not in [States.LOADING.state, States.MAIN.state]:
        return

    last_round, last_player_id = player.parameters.get("last_round", None), player.parameters.get(
        "last_player_id", None
    )
    await state.set_state(state=States.MAIN)
    engine = poker.engine.to_original()
    if (
        last_round is None
        or int(last_round) != engine.round.value  # noqa
        or last_player_id is None
        or last_player_id != engine.current_player.id
    ):
        player.parameters = {
            **player.parameters,
            "last_round": engine.round.value,
            "last_player_id": engine.current_player.id,
        }
        await send_main_state_message(bot=bot, engine=engine, cards=poker.cards, player=player)
