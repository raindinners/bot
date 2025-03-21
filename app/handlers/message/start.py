from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import Message

router = Router()


@router.message(CommandStart(), StateFilter(any_state))
async def start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text="Hello! With my help you can in games!")
    await state.clear()
