from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis

from handlers import setup_handlers


def create_dispatcher() -> Dispatcher:
    redis = Redis()
    scheduler = AsyncIOScheduler()
    storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True))
    dispatcher = Dispatcher(storage=storage, redis=redis, scheduler=scheduler)

    @dispatcher.startup()
    async def startup() -> None:
        scheduler.start()

    @dispatcher.shutdown()
    async def shutdown() -> None:
        scheduler.shutdown()

    handlers_router = setup_handlers()
    dispatcher.include_router(handlers_router)

    return dispatcher
