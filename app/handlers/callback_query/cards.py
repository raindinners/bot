from __future__ import annotations

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import CardsCallbackData
from core.poker.schema import Poker
from filters import PokerFilter
from states import States

router = Router()


@router.callback_query(
    CardsCallbackData.filter(),
    StateFilter(States.MAIN),
    PokerFilter(),
)
async def cards_handler(callback_query: CallbackQuery, poker: Poker) -> None:
    hand = poker.cards.hands[poker.engine.current.value]
    await callback_query.answer(text=f"{hand.front.string} {hand.back.string}", show_alert=True)
