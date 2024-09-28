from __future__ import annotations

import random
from contextlib import suppress

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pokerengine.engine import EngineTraits
from redis.asyncio import Redis

from _redis import save
from callback_data import CreateCallbackData
from core.poker import game
from enums.games import Games
from keyboards import poker_inline_keyboard_builder
from metadata import (
    BB_BET,
    BB_MULT,
    MIN_RAISE,
    RANDOM_MAX_VALUE,
    RANDOM_MIN_VALUE,
    SB_BET,
)
from poker import Poker

router = Router()


@router.callback_query(CreateCallbackData.filter(F.game == Games.POKER.name))
async def create_dig_handler(
    callback_query: CallbackQuery,
    bot: Bot,
    scheduler: AsyncIOScheduler,
    redis: Redis,
) -> None:
    await save(
        redis=redis,
        key=callback_query.inline_message_id,
        value=Poker(
            traits=EngineTraits(
                sb_bet=SB_BET,
                bb_bet=BB_BET,
                bb_mult=BB_MULT,
                min_raise=MIN_RAISE,
            ),
            seed=random.randint(RANDOM_MIN_VALUE, RANDOM_MAX_VALUE),
        ),
    )
    scheduler.add_job(
        game,
        kwargs={
            "bot": bot,
            "redis": redis,
            "inline_message_id": callback_query.inline_message_id,
        },
        trigger="interval",
        id=callback_query.inline_message_id,
        max_instances=1,
        seconds=1,
    )

    with suppress(TelegramBadRequest):
        await bot.edit_message_reply_markup(
            inline_message_id=callback_query.inline_message_id,
            reply_markup=poker_inline_keyboard_builder(
                inline_message_id=callback_query.inline_message_id
            ).as_markup(),
        )

    await callback_query.answer(text="Created!")
