from __future__ import annotations

from contextlib import suppress
from typing import List, Optional

from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import CallbackQuery
from pokerengine.engine import PlayerAction
from pokerengine.enums import ActionE
from redis.asyncio import Redis

from _redis import save
from callback_data import ActionCallbackData
from enums import Action
from keyboards import (
    information_inline_keyboard_builder,
    pin_inline_keyboard_builder,
    player_cards_inline_keyboard_builder,
)
from utils.poker import get_poker

router = Router()


def find_action(actions: List[PlayerAction], action: ActionE) -> Optional[PlayerAction]:
    for _action in actions:
        if _action.action == action:
            return _action

    return None


@router.callback_query(ActionCallbackData.filter(), StateFilter(any_state))
async def actions_handler(
    callback_query: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    redis: Redis,
    callback_data: ActionCallbackData,
) -> None:
    poker = await get_poker(redis=redis, poker=callback_query.inline_message_id)

    current_player_id, _current_player_name = poker.engine.positions.player.id.split("_")
    if callback_query.from_user.id != int(current_player_id):
        await callback_query.answer(text="Not your button!")
        return

    actions = poker.engine.actions.actions
    match Action(callback_data.action):
        case Action.FOLD:
            fold = find_action(actions=actions, action=ActionE.FOLD)
            if not fold:
                await callback_query.answer(text="There is no Fold")
                return

            poker.execute(action=fold)
            await callback_query.answer(text="Executed!")
        case Action.CHECK:
            check = find_action(actions=actions, action=ActionE.CHECK)
            if not check:
                await callback_query.answer(text="There is no Check")
                return

            poker.execute(action=check)
            await callback_query.answer(text="Executed!")
        case Action.CALL:
            call = find_action(actions=actions, action=ActionE.CALL)
            if not call:
                await callback_query.answer(text="There is no Call")
                return

            poker.execute(action=call)
            await callback_query.answer(text="Executed!")
        case Action.BET:
            bet = find_action(actions=actions, action=ActionE.BET)
            if not bet:
                await callback_query.answer(text="There is no Bet")
                return

            await state.update_data(
                current_player_id=int(current_player_id),
                action=Action.BET.value,
                amount=bet.amount,
            )
            with suppress(TelegramBadRequest):
                await bot.edit_message_reply_markup(
                    inline_message_id=callback_query.inline_message_id,
                    reply_markup=player_cards_inline_keyboard_builder(
                        inline_message_id=callback_query.inline_message_id
                    )
                    .attach(
                        information_inline_keyboard_builder(
                            inline_message_id=callback_query.inline_message_id
                        )
                    )
                    .attach(
                        pin_inline_keyboard_builder(
                            inline_message_id=callback_query.inline_message_id
                        )
                    )
                    .as_markup(),
                )
            await callback_query.answer(text="Enter amount!")
        case Action.RAISE:
            if not find_action(actions=actions, action=ActionE.RAISE):
                await callback_query.answer(text="There is no Raise")
                return

            await state.update_data(
                current_player_id=int(current_player_id),
                action=Action.RAISE.value,
                amount=poker.engine.traits.min_raise,
            )
            with suppress(TelegramBadRequest):
                await bot.edit_message_reply_markup(
                    inline_message_id=callback_query.inline_message_id,
                    reply_markup=player_cards_inline_keyboard_builder(
                        inline_message_id=callback_query.inline_message_id
                    )
                    .attach(
                        information_inline_keyboard_builder(
                            inline_message_id=callback_query.inline_message_id
                        )
                    )
                    .attach(
                        pin_inline_keyboard_builder(
                            inline_message_id=callback_query.inline_message_id
                        )
                    )
                    .as_markup(),
                )
            await callback_query.answer(text="Enter amount!")
        case _:
            allin = find_action(actions=actions, action=ActionE.ALLIN)
            if not allin:
                await callback_query.answer(text="There is no Allin")
                return

            poker.execute(action=allin)
            await callback_query.answer(text="Executed!")
    await save(redis=redis, key=callback_query.inline_message_id, value=poker)
