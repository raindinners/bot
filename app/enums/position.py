from __future__ import annotations

from ._enum import Enum


class Position(Enum):
    """
    Represents player position in the game.
    """

    NONE = -1
    SB = 0
    BB = 1
    UTG = 2
    LWJ = 3
    HIJ = 4
    COF = 5
    BTN = 6
