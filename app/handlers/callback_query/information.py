from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from redis.asyncio import Redis

from callback_data import InformationCallbackData
from enums import Position, State
from utils.poker import get_player_by_id, get_player_position, get_poker

router = Router()


@router.callback_query(InformationCallbackData.filter())
async def information_handler(
    callback_query: CallbackQuery,
    redis: Redis,
    callback_data: InformationCallbackData,
) -> None:
    poker = await get_poker(redis=redis, poker=callback_data.inline_message_id)

    player = get_player_by_id(
        poker=poker, id_=f"{callback_query.from_user.id}_{callback_query.from_user.first_name}"
    )
    if not player:
        await callback_query.answer("You are not in the game!")
        return

    position = get_player_position(poker=poker, player=player)
    await callback_query.answer(
        text=f"Position: {Position(position.value).as_string()}"
        f"\n"
        f"State: {State(player.state.value).as_string()}"
        f"\n"
        f"Round Bet: {player.round_bet} | Total Chips {player.behind}"
        f"\n"
        f"Is Left: {player.is_left}",
        show_alert=True,
    )
