from __future__ import annotations

from .schema import ApplicationSchema


class Player(ApplicationSchema):
    id: str
    is_left: bool
    stack: int
    behind: int
    front: int
    round_bet: int
    state: int
