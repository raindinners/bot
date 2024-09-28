from __future__ import annotations

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import CallbackQuery
from pokerengine.engine import PlayerAction
from pokerengine.enums import ActionE
from redis.asyncio import Redis

from _redis import save
from callback_data import PinCallbackData
from logger import logger
from utils.poker import get_poker

router = Router()


@router.callback_query(PinCallbackData.filter(), StateFilter(any_state))
async def pin_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    redis: Redis,
    callback_data: PinCallbackData,
) -> None:
    data = await state.get_data()
    if (
        not (current_player_id := data.get("current_player_id", 0))
        or int(current_player_id) != callback_query.from_user.id
    ):
        await callback_query.answer(text="Not your button!")
        return

    amount = data.get("amount", str())
    if callback_data.data == "no":
        return
    if callback_data.data == "amount":
        await callback_query.answer(text=f"Amount: {amount if amount else 0}")
        return
    if callback_data.data == "C":
        amount = str()
    elif callback_data.data == "=" and amount:
        poker = await get_poker(redis=redis, poker=callback_query.inline_message_id)
        try:
            poker.execute(
                action=PlayerAction(
                    action=ActionE(int(data.get("action"))),
                    position=poker.engine.positions.current,
                    amount=int(amount),
                )
            )
        except Exception:  # noqa
            await callback_query.answer(text="Invalid action amount!", show_alert=True)
            return
        finally:
            data["amount"] = str()
            data["action"] = None
            await save(redis=redis, key=callback_query.inline_message_id, value=poker)
    elif callback_data.data == "<<" or callback_data.data == ">>":
        data["amount"] = str()
        data["action"] = None

        poker = await get_poker(redis=redis, poker=callback_query.inline_message_id)
        poker.current_round = poker.current_round - 1
        await save(redis=redis, key=callback_query.inline_message_id, value=poker)

        await callback_query.answer(text="Going back...")
    elif callback_data.data == "<" and amount:
        amount = str().join(amount.rsplit(amount[-1], 1))
    else:
        logger.critical("AMOUNT")
        amount += str() if not amount and callback_data.data == "0" else callback_data.data

    data["amount"] = amount
    await state.update_data(data=data)
    await callback_query.answer(text=f"Amount: {amount if amount else 0}")
