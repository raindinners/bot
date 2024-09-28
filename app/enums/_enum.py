from __future__ import annotations

from enum import Enum as BaseEnum
from typing import Any


class Enum(BaseEnum):
    def __init__(self, value: Any) -> None:
        if hasattr(value, "value"):
            value = value.value

        super().__init__(value)

    def as_string(self) -> str:
        return self.name.lower().capitalize()
