from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio.client import Redis

from core.settings import fsm_settings
from handlers import setup_handlers


def create_dispatcher() -> Dispatcher:
    redis = Redis(host=fsm_settings.FSM_HOSTNAME, port=fsm_settings.FSM_PORT)
    scheduler = AsyncIOScheduler()

    dispatcher = Dispatcher(storage=RedisStorage(redis=redis), redis=redis, scheduler=scheduler)

    @dispatcher.startup()
    async def startup() -> None:
        scheduler.start()

    @dispatcher.shutdown()
    async def shutdown() -> None:
        scheduler.shutdown()

    handlers_router = setup_handlers()
    dispatcher.include_router(handlers_router)

    return dispatcher
