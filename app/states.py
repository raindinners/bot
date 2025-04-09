from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    ACTIONS = State()
    DEFAULT = State()
    LOADING = State()
    MAIN = State()
    PIN = State()
