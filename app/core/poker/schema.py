from __future__ import annotations

from typing import Optional

from pokerengine.card import CardGenerator
from pokerengine.card import Cards as CardsOriginal
from pokerengine.constants import BOARD_SIZE, HAND_SIZE
from pokerengine.schema import Cards, EngineRake01
from pydantic import BaseModel


class Poker(BaseModel):
    id: str
    engine: EngineRake01
    seed: int = 1927
    started: bool = False
    start_at: Optional[float] = None
    auto_action_time: Optional[float] = None
    winners_time: Optional[float] = None
    cards: Optional[Cards] = None

    def start(self) -> None:
        self.started = True
        self.start_at = None
        self.auto_action_time = None
        self.winners_time = None

        engine = self.engine.to_original()
        engine.start(is_new_game=bool(self.cards))
        self.engine = EngineRake01.from_original(engine)

        self.cards = Cards.from_original(
            CardsOriginal(
                cards=CardGenerator(seed=self.seed).generate_v(
                    BOARD_SIZE + (len(self.engine.players) * HAND_SIZE)
                )
            )
        )

    def stop(self) -> None:
        self.started = False
        self.start_at = None
        self.auto_action_time = None
        self.winners_time = None

        engine = self.engine.to_original()
        engine.stop()
        self.engine = EngineRake01.from_original(engine)
