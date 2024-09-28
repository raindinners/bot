from __future__ import annotations

from .schema import ApplicationSchema


class Action(ApplicationSchema):
    amount: int
    action: int
    position: int
