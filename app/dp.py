from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pokerengine.pretty_string import PrettyCard
from redis.asyncio import Redis

from core.settings import redis_settings
from handlers import setup_handlers
from middleware import PokerAutoSaverMiddleware


def create_dispatcher() -> Dispatcher:
    redis = Redis.from_url(url=redis_settings.REDIS_URL)
    scheduler = AsyncIOScheduler()
    storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True))
    dispatcher = Dispatcher(
        storage=storage, redis=redis, scheduler=scheduler, pretty_card=PrettyCard()
    )

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
