from __future__ import annotations

from aiogram import Router

from .start import router as start_router


def setup() -> Router:
    router = Router()
    router.include_routers(start_router)

    return router
