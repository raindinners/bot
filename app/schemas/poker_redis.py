from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .schema import ApplicationSchema

if TYPE_CHECKING:
    from .card import Cards
    from .player import Player
    from .traits import Traits


class PokerRedis(ApplicationSchema):
    preview_round: int = -1
    traits: Traits
    players: List[Player]
    position: int
    round: int
    flop_dealt: bool
    seed: int
    started: bool
    start_at: Optional[float]
    winners_time: Optional[float]
    cards: Optional[Cards]
