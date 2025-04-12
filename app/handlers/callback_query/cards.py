from __future__ import annotations

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from pokerengine.pretty_string import PrettyCard

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
async def cards_handler(
    callback_query: CallbackQuery, poker: Poker, pretty_card: PrettyCard
) -> None:
    player_index = None
    for index, player in enumerate(poker.engine.players):
        if int(player.id) == callback_query.from_user.id:
            player_index = index

    hand = poker.cards.hands[player_index]
    await callback_query.answer(
        text=f"{pretty_card.as_pretty_string(value=hand.front)} {pretty_card.as_pretty_string(value=hand.back)}",
        show_alert=True,
    )
