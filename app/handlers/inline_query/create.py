from __future__ import annotations

from typing import Any, List

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from enums.games import Games
from keyboards import create_inline_keyboard_builder
from utils.inline_query import get_id

router = Router()


async def get_results() -> List[Any]:
    return [
        InlineQueryResultArticle(
            id=get_id(),
            title=game,
            input_message_content=InputTextMessageContent(
                message_text=game, parse_mode=ParseMode.MARKDOWN
            ),
            reply_markup=create_inline_keyboard_builder(game=game).as_markup(),
        )
        for game in Games
    ]


@router.inline_query()
async def create_handler(inline_query: InlineQuery) -> None:
    await inline_query.answer(  # mypy: ignore[arg-type]
        results=await get_results(),
        is_personal=True,
    )
