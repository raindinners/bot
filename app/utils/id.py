from __future__ import annotations

import os
import random

from aiogram.types import User

from metadata import MAX_ID_VALUE, MIN_ID_VALUE, URANDOM_SIZE


def generate_id() -> str:
    return os.urandom(URANDOM_SIZE).hex()


def get_inline_query_id() -> str:
    return str(random.uniform(MIN_ID_VALUE, MAX_ID_VALUE))


def get_player_id(user: User) -> str:
    return user.mention_markdown(name=user.full_name)
