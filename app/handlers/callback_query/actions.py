from __future__ import annotations

from typing import Any, Dict

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from pokerengine.engine import EngineRake01, PlayerAction
from pokerengine.enums import Action, Position

from callback_data import ActionsCallbackData
from core.poker.schema import Poker
from filters import CurrentOrderFilter, PokerFilter, StateDataUnpackerFilter
from messages import send_actions_state_message, send_main_state_message
from states import States

router = Router()


@router.callback_query(
    ActionsCallbackData.filter(F.is_done.is_(False)),
    StateFilter(States.MAIN),
    StateDataUnpackerFilter(),
    PokerFilter(),
    CurrentOrderFilter(),
)
async def actions_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    state_data: Dict[str, Any],
    engine: EngineRake01,
) -> None:
    if engine.terminal_state or engine.showdown:
        await callback_query.answer(text="Unavailable")

    await send_actions_state_message(
        bot=callback_query.bot,
        engine=engine,
        selected_action=state_data.get("selected_action", None),  # noqa
    )
    await state.set_state(state=States.ACTIONS)


@router.callback_query(
    ActionsCallbackData.filter(F.is_done.is_(True)),
    StateFilter(States.ACTIONS),
    StateDataUnpackerFilter(),
    PokerFilter(),
    CurrentOrderFilter(),
)
async def actions_done_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    state_data: Dict[str, Any],
    poker: Poker,
    engine: EngineRake01,
) -> None:
    player = engine.current_player

    selected_action = state_data.get("selected_action", None)
    if selected_action is not None:
        engine.execute(
            player_action=PlayerAction(
                action=Action(int(selected_action["action"])),
                position=Position(int(selected_action["position"])),
                amount=int(selected_action["amount"]),
            )
        )
    else:
        await send_main_state_message(
            bot=callback_query.bot, engine=engine, cards=poker.cards, player=player
        )

    await state.set_state(state=States.MAIN)
