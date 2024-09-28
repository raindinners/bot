from __future__ import annotations

from aiogram import Router

from .actions import router as actions_router
from .create import router as create_router
from .information import router as information_router
from .pin import router as pin_router
from .player_cards import router as player_cards_router
from .poker import router as poker_router


def setup() -> Router:
    router = Router()
    router.include_routers(
        actions_router,
        create_router,
        information_router,
        pin_router,
        player_cards_router,
        poker_router,
    )

    return router
