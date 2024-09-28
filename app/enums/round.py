from __future__ import annotations

from ._enum import Enum


class Round(Enum):
    """
    Represents game round.
    """

    NONE = -1
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4
