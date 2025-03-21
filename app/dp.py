from __future__ import annotations

from aiogram import Dispatcher

from handlers import setup_handlers


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()

    @dispatcher.startup()
    async def startup() -> None:
        scheduler.start()

    @dispatcher.shutdown()
    async def shutdown() -> None:
        scheduler.shutdown()

    handlers_router = setup_handlers()
    dispatcher.include_router(handlers_router)

    return dispatcher
