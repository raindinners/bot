from __future__ import annotations

from aiogram import Router

from .actions import router as actions_router
from .cards import router as cards_router
from .pin import router as pin_router
from .poker import router as poker_router
from .selected_action import router as selected_action_router


def setup() -> Router:
    router = Router()
    router.include_routers(
        actions_router, cards_router, pin_router, poker_router, selected_action_router
    )

    return router
