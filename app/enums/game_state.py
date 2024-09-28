from __future__ import annotations

from ._enum import Enum


class GameState(str, Enum):
    STARTING = "STARTING"
    STOPPED = "STOPPED"
    STARTED = "STARTED"
    ACTIONS = "ACTIONS"
    AUTO = "AUTO"
