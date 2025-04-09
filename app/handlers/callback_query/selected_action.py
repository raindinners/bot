from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from pokerengine import enums_schema
from pokerengine.engine import EngineRake01
from pokerengine.enums import Action, Position

from callback_data import SelectActionCallbackData
from filters import CurrentOrderFilter, PokerFilter
from messages import send_actions_state_message, send_pin_state_message
from states import States

router = Router()


@router.callback_query(
    SelectActionCallbackData.filter(
        F.action.in_(
            [
                enums_schema.Action.FOLD.value,
                enums_schema.Action.CHECK.value,
                enums_schema.Action.CALL.value,
            ]
        )
    ),
    StateFilter(States.ACTIONS),
    PokerFilter(),
    CurrentOrderFilter(),
)
async def select_action_no_amount_handler(
    callback_query: CallbackQuery,
    callback_data: SelectActionCallbackData,
    state: FSMContext,
    engine: EngineRake01,
) -> None:
    await state.update_data(
        selected_action={
            "action": Action(callback_data.action).value,
            "position": Position(callback_data.position).value,
            "max_amount": callback_data.amount,
            "amount": callback_data.amount,
        }
    )

    await send_actions_state_message(
        bot=callback_query.bot,
        engine=engine,
        selected_action=(await state.get_data())["selected_action"],
    )
    await callback_query.answer(
        text=f"Action: {Action(callback_data.action).name.capitalize()} successfully selected."
    )


@router.callback_query(
    SelectActionCallbackData.filter(
        F.action.in_([enums_schema.Action.BET.value, enums_schema.Action.RAISE.value])
    ),
    StateFilter(States.ACTIONS),
    PokerFilter(),
    CurrentOrderFilter(),
)
async def select_action_with_amount_handler(
    callback_query: CallbackQuery,
    callback_data: SelectActionCallbackData,
    state: FSMContext,
    engine: EngineRake01,
) -> None:
    await state.update_data(
        selected_action={
            "action": Action(callback_data.action).value,
            "position": Position(callback_data.position).value,
            "max_amount": callback_data.amount,
            "amount": "0",
        }
    )

    await send_pin_state_message(bot=callback_query.bot, engine=engine)
    await callback_query.answer(
        text=f"Action: {Action(callback_data.action).name.capitalize()} successfully selected, provide amount."
    )

    await state.set_state(state=States.PIN)
