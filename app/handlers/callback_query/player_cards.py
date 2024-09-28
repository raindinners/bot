from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from redis.asyncio import Redis

from callback_data import PlayerCardsCallbackData
from schemas import Card, Hand, PlayerCards
from utils.poker import get_player_by_id, get_player_position, get_poker

router = Router()


@router.callback_query(PlayerCardsCallbackData.filter())
async def player_cards_handler(
    callback_query: CallbackQuery,
    redis: Redis,
    callback_data: PlayerCardsCallbackData,
) -> None:
    poker = await get_poker(redis=redis, poker=callback_data.inline_message_id)

    player = get_player_by_id(
        poker=poker, id_=f"{callback_query.from_user.id}_{callback_query.from_user.first_name}"
    )
    if not player:
        await callback_query.answer("You are not in the game!")
        return

    hand = poker.cards.hands[get_player_position(poker=poker, player=player).value]
    hand = PlayerCards(
        hand=Hand(
            back=Card(value=hand.value[0].card, string=str(hand.value[0])),
            front=Card(value=hand.value[1].card, string=str(hand.value[1])),
        )
    )
    await callback_query.answer(
        text=f"Back: {hand.hand.back.string.upper().replace('C', '♣️').replace('D', '♦️').replace('H', '♥️').replace('S', '♠️')}"
        f"\n"
        f"Front: {hand.hand.front.string.upper().replace('C', '♣️').replace('D', '♦️').replace('H', '♥️').replace('S', '♠️')}",
        show_alert=True,
    )
