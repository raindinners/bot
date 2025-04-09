from __future__ import annotations

from typing import Any, List

from aiogram import F, Router
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from aiogram.utils.formatting import Text

from callback_data import PokerCallbackData
from utils.inline_query import get_id

router = Router()


async def get_results() -> List[Any]:
    return [
        InlineQueryResultArticle(
            id=get_id(),
            title="Poker",
            input_message_content=InputTextMessageContent(
                **Text("Push down...").as_kwargs(text_key="message_text"),
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Poker", callback_data=PokerCallbackData().pack())]
                ]
            ),
        )
    ]


@router.inline_query(F.query == "create")
async def create_handler(inline_query: InlineQuery) -> None:
    await inline_query.answer(results=await get_results(), is_personal=True)
