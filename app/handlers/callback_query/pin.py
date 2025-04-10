from __future__ import annotations

from typing import Any, Dict

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from pokerengine.engine import EngineRake01

from callback_data import PinCallbackData
from filters import CurrentOrderFilter, PokerFilter, StateDataUnpackerFilter
from messages import send_actions_state_message
from states import States

router = Router()


@router.callback_query(
    PinCallbackData.filter(),
    StateFilter(States.PIN),
    StateDataUnpackerFilter(),
    PokerFilter(),
    CurrentOrderFilter(),
)
async def pin_handler(
    callback_query: CallbackQuery,
    callback_data: PinCallbackData,
    state: FSMContext,
    state_data: Dict[str, Any],
    engine: EngineRake01,
) -> None:
    selected_action = state_data["selected_action"]

    match callback_data.action:
        case "add":
            selected_action["amount"] = (
                callback_data.argument
                if selected_action["amount"] == "0" and callback_data.argument != "0"
                else (
                    selected_action["amount"]
                    + (
                        str()
                        if selected_action["amount"] == "0" and callback_data.argument == "0"
                        else callback_data.argument
                    )
                )
            )
        case "remove":
            selected_action["amount"] = selected_action["amount"][:-1]
            if not selected_action["amount"]:
                selected_action["amount"] = "0"
        case "apply":
            amount = int(selected_action["amount"])
            if engine.engine_traits.bb_bet > amount or amount > int(selected_action["max_amount"]):
                await callback_query.answer(text="Invalid amount entered, retype.")
                return
            await state.set_state(state=States.ACTIONS)
            await send_actions_state_message(
                bot=callback_query.bot, engine=engine, selected_action=selected_action
            )
            return

    await callback_query.answer(text=f"Amount: {selected_action['amount']}")
    await state.update_data(selected_action=selected_action)
