from __future__ import annotations

from aiogram import Bot, Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import any_state
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pokerengine import schema
from pokerengine.engine import EngineRake01, EngineTraits
from pokerengine.pretty_string import PrettyCard
from redis.asyncio import Redis

from callback_data import PokerCallbackData
from core.poker.core import poker_main_job
from core.poker.schema import Poker
from messages import Messages
from metadata import BB_BET, BB_MULT, MIN_RAISE, SB_BET
from utils.id import generate_id

router = Router()


@router.callback_query(PokerCallbackData.filter(), StateFilter(any_state))
async def poker_handler(
    callback_query: CallbackQuery,
    bot: Bot,
    redis: Redis,
    scheduler: AsyncIOScheduler,
    pretty_card: PrettyCard,
) -> None:
    engine = EngineRake01(
        engine_traits=EngineTraits(
            sb_bet=SB_BET, bb_bet=BB_BET, bb_mult=BB_MULT, min_raise=MIN_RAISE
        )
    )

    poker = Poker(
        id=f"poker_{generate_id()}", engine=schema.EngineRake01.from_original(value=engine)
    )
    await redis.set(name=poker.id, value=poker.model_dump_json())

    messages = Messages(
        bot=bot,
        poker_id=poker.id,
        inline_message_id=callback_query.inline_message_id,
        pretty_card=pretty_card,
    )
    scheduler.add_job(
        poker_main_job,
        kwargs={"poker": poker, "redis": redis, "messages": messages},
        trigger="interval",
        id=poker.id,
        max_instances=1,
        seconds=1,
    )
    await messages.send_join()
    await messages.send_join_keyboard()
