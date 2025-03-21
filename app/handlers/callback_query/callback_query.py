from __future__ import annotations

from aiogram import Router

from .pin import router as pin_router


def setup() -> Router:
    router = Router()
    router.include_routers(pin_router)

    return router
