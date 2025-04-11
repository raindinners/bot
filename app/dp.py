from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.base import DefaultKeyBuilder, StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pokerengine.pretty_string import PrettyCard
from redis.asyncio import Redis

from core.poker.schema import Poker
from core.settings import redis_settings
from handlers import setup_handlers
from logger import logger
from middleware import PokerAutoSaverMiddleware


def create_dispatcher() -> Dispatcher:
    redis = Redis()
    scheduler = AsyncIOScheduler()
    storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True))
    dispatcher = Dispatcher(
        storage=storage, redis=redis, scheduler=scheduler, pretty_card=PrettyCard()
    )

    @dispatcher.startup()
    async def startup_remove_poker() -> None:
        async for name in redis.scan_iter(match="poker_*"):
            poker = Poker.model_validate_json(await redis.get(name=name))

            for player in poker.engine.players:
                key = StorageKey(
                    bot_id=int(player.parameters["bot_id"]),  # noqa
                    chat_id=int(player.parameters["chat_id"]),  # noqa
                    user_id=int(player.parameters["user_id"]),  # noqa
                )
                await storage.set_data(key=key, data=dict())
                await storage.set_state(key=key)
            await redis.delete(name)

    @dispatcher.startup()
    async def startup() -> None:
        scheduler.start()

    @dispatcher.shutdown()
    async def shutdown() -> None:
        scheduler.shutdown()

    handlers_router = setup_handlers()
    dispatcher.include_router(handlers_router)

    poker_auto_saver_middleware = PokerAutoSaverMiddleware()
    dispatcher.callback_query.middleware.register(middleware=poker_auto_saver_middleware)
    dispatcher.message.middleware.register(middleware=poker_auto_saver_middleware)

    return dispatcher
