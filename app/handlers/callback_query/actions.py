from __future__ import annotations

from typing import Any, Dict

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from pokerengine.engine import EngineRake01, PlayerAction
from pokerengine.enums import Action, Position
from pokerengine.pretty_string import PrettyCard

from callback_data import ActionsCallbackData
from core.poker.schema import Poker
from filters import CurrentOrderFilter, PokerFilter, StateDataUnpackerFilter
from messages import Messages
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
    bot: Bot,
    state: FSMContext,
    state_data: Dict[str, Any],
    engine: EngineRake01,
) -> None:
    if engine.showdown:
        await callback_query.answer(text="Unavailable")
        return

    messages = Messages(bot=bot)
    await messages.send_actions_state(
        engine=engine, selected_action=state_data.get("selected_action", None)
    )  # noqa
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
    bot: Bot,
    state: FSMContext,
    state_data: Dict[str, Any],
    poker: Poker,
    engine: EngineRake01,
    pretty_card: PrettyCard,
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
        messages = Messages(bot=bot, pretty_card=pretty_card, player=player)
        await messages.send_main_state(poker=poker, engine=engine, cards=poker.cards)
        await messages.send_main_state_keyboard()

    await state.set_state(state=States.MAIN)
