from __future__ import annotations

from aiogram import Bot
from redis.asyncio import Redis

from _redis import save
from logger import logger
from poker import Poker
from utils.poker import get_poker

from .information import information
from .start import start
from .winners import winners


async def core(bot: Bot, inline_message_id: str, poker: Poker) -> None:
    await winners(bot=bot, inline_message_id=inline_message_id, poker=poker)
    await start(bot=bot, inline_message_id=inline_message_id, poker=poker)
    await information(bot=bot, inline_message_id=inline_message_id, poker=poker)


async def game(bot: Bot, redis: Redis, inline_message_id: str) -> None:
    poker = await get_poker(redis=redis, poker=inline_message_id)

    try:
        await core(bot=bot, inline_message_id=inline_message_id, poker=poker)
    except Exception as exc:
        logger.exception(exc)

    await save(redis=redis, key=inline_message_id, value=poker)
