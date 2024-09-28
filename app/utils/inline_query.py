from __future__ import annotations

from random import uniform
from typing import Final

_MIN_VALUE: Final[int] = 2**16
_MAX_VALUE: Final[int] = 2**32


def get_id() -> str:
    return str(uniform(_MIN_VALUE, _MAX_VALUE))
