from __future__ import annotations

from random import uniform

from metadata import MAX_ID_VALUE, MIN_ID_VALUE


def get_id() -> str:
    return str(uniform(MIN_ID_VALUE, MAX_ID_VALUE))
