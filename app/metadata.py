from __future__ import annotations

from typing import Final

URANDOM_SIZE: Final[int] = 8
"""Using in function: `os.random` as `__size` argument."""

SB_BET: Final[int] = 50
"""Small blind bet."""
BB_BET: Final[int] = 100
"""Big blind bet."""
BB_MULT: Final[int] = 15
"""Big blind x big blind mult for calculating stack size."""
MIN_RAISE: Final[int] = 200
"""Min raise."""

MIN_ID_VALUE: Final[int] = 2**16
MAX_ID_VALUE: Final[int] = 2**32

POKER_START_TIME: Final[int] = 1
"""Start game after time (in seconds)."""

POKER_WINNERS_TIME: Final[int] = 10
"""How many time winners will be displaying (in seconds)."""

RANDOM_MIN_VALUE: Final[int] = 0
"""Seed random min value."""

RANDOM_MAX_VALUE: Final[int] = 65535
"""Seed random max value"""
