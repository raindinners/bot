from __future__ import annotations

from typing import Final, Type, Union

from pokerengine.engine import EngineRake01

ENGINE_CLASS: Type[Union[EngineRake01]] = EngineRake01
"""Engine base class."""

START_TIME: Final[int] = 5
"""Start game after time (in seconds)."""

WINNERS_TIME: Final[int] = 10
"""How many time winners will be displaying (in seconds)."""

AUTO_ACTION_TIME: Final[int] = 10
"""Time to wait until player did a move (in seconds)."""

SB_BET: Final[int] = 50
"""Small blind bet."""

BB_BET: Final[int] = 100
"""Big blind bet."""

BB_MULT: Final[int] = 15
"""Big blind x big blind mult for calculating stack size."""

MIN_RAISE: Final[int] = 100
"""Min raise."""

RANDOM_MIN_VALUE: Final[int] = 0
"""Seed random min value."""

RANDOM_MAX_VALUE: Final[int] = 65535
"""Seed random max value"""
