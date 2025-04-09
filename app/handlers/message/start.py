from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    SwitchInlineQueryChosenChat,
)
from aiogram.utils.formatting import Bold
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pokerengine import schema
from redis.asyncio import Redis

from core.poker.core import poker_chat_job
from core.poker.schema import Poker
from metadata import BB_BET, BB_MULT
from states import States
from utils.id import get_player_id
from utils.inline_query import get_id

router = Router()


@router.message(CommandStart(deep_link=True), StateFilter(default_state))
async def start_deep_link_handler(
    message: Message,
    state: FSMContext,
    command: CommandObject,
    redis: Redis,
    scheduler: AsyncIOScheduler,
) -> None:
    new_message = await message.answer(
        **Bold("Poker created. Wait until game starts.").as_kwargs()
    )

    poker = Poker.model_validate_json(await redis.get(name=command.args))
    engine = poker.engine.to_original()

    joined_player = None
    player_id = get_player_id(user=message.from_user)
    engine.add_player(stack=BB_BET * BB_MULT, id=player_id)
    for player in engine.players:
        if player.id == player_id:
            joined_player = player
            player.parameters = {
                "chat_id": new_message.chat.id,
                "message_id": new_message.message_id,
            }

    await state.update_data(poker=command.args)
    poker.engine = schema.EngineRake01.from_original(value=engine)

    await redis.set(name=poker.id, value=poker.model_dump_json())
    await state.set_state(state=States.LOADING)

    scheduler.add_job(
        poker_chat_job,
        kwargs={
            "bot": message.bot,
            "player": joined_player,
            "poker": poker,
            "state": state,
            "redis": redis,
        },
        trigger="interval",
        id=get_id(),
        max_instances=1,
        seconds=1,
    )


@router.message(CommandStart(deep_link=False))
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        **Bold("Welcome to Poker!").as_kwargs(),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Create",
                        switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat(
                            query="create",
                            allow_user_chats=True,
                            allow_bot_chats=False,
                            allow_group_chats=True,
                            allow_channel_chats=False,
                        ),
                    )
                ]
            ],
        ),
    )
