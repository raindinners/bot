from __future__ import annotations

from typing import Optional

from pokerengine.card import CardGenerator
from pokerengine.card import Cards as PCards
from pokerengine.constants import BOARD_SIZE, HAND_SIZE
from pokerengine.engine import EngineTraits
from pokerengine.engine import Player as PPlayer
from pokerengine.engine import PlayerAction
from pokerengine.enums import PositionE, RoundE, StateE

from metadata import ENGINE_CLASS
from schemas import Card, Cards, Hand, Player, PokerRedis, Traits


class Poker:
    def __init__(
        self,
        traits: EngineTraits,
        *,
        preview_round: int = -1,
        seed: int = 1927,
        started: bool = False,
        start_at: Optional[float] = None,
        winners_time: Optional[float] = None,
        cards: Optional[PCards] = None,
    ) -> None:
        self.preview_round = preview_round

        self.started: bool = started
        self.start_at: Optional[float] = start_at

        self.winners_time: Optional[float] = winners_time

        self.cards: Optional[PCards] = cards

        self.seed = seed
        self.cards_generator = CardGenerator(seed=self.seed)

        self.engine = ENGINE_CLASS(traits=traits)

    def start(self) -> None:
        self.preview_round = -1
        self.started = True
        self.start_at = None
        self.winners_time = None
        self.engine.start(new_game=bool(self.cards))
        self.cards = PCards(
            cards=self.cards_generator.generate_v(
                BOARD_SIZE + len(self.engine.players.players) * HAND_SIZE
            )
        )

    def stop(self) -> None:
        self.preview_round = -1
        self.started = False
        self.start_at = None
        self.winners_time = None
        self.engine.stop()

    def execute(self, action: PlayerAction) -> None:
        self.engine.actions.execute(action=action)
        self.preview_round -= 1

    def _encode(self) -> str:
        return PokerRedis(
            preview_round=self.preview_round,
            traits=Traits.model_validate(self.engine.traits),
            players=[Player.model_validate(player) for player in self.engine.players.players],
            position=self.engine.positions.current,
            round=self.engine.round.round,
            flop_dealt=self.engine.round.flop_dealt,
            seed=self.seed,
            started=self.started,
            start_at=self.start_at,
            winners_time=self.winners_time,
            cards=(
                Cards(
                    board=[Card(value=card.card, string=str(card)) for card in self.cards.board],
                    hands=[
                        Hand(
                            front=Card(value=hand.value[0].card, string=str(hand.value[0])),
                            back=Card(value=hand.value[1].card, string=str(hand.value[1])),
                        )
                        for hand in self.cards.hands
                    ],
                )
                if self.cards
                else None
            ),
        ).model_dump_json()

    @classmethod
    def _decode(cls, value: str) -> Poker:
        encoded = PokerRedis.model_validate_json(value)

        poker = cls(
            preview_round=encoded.preview_round,
            traits=EngineTraits(
                sb_bet=encoded.traits.sb_bet,
                bb_bet=encoded.traits.bb_bet,
                bb_mult=encoded.traits.bb_mult,
                min_raise=encoded.traits.min_raise,
            ),
            seed=encoded.seed,
            started=encoded.started,
            start_at=encoded.start_at,
            winners_time=encoded.winners_time,
            cards=(
                PCards(
                    board=[card.string for card in encoded.cards.board],
                    hands=[hand.front.string + hand.back.string for hand in encoded.cards.hands],
                )
                if encoded.cards
                else None
            ),
        )
        poker.engine.load(
            traits=EngineTraits(
                sb_bet=encoded.traits.sb_bet,
                bb_bet=encoded.traits.bb_bet,
                bb_mult=encoded.traits.bb_mult,
                min_raise=encoded.traits.min_raise,
            ),
            players=[
                PPlayer(
                    is_left=player.is_left,
                    stack=player.stack,
                    behind=player.behind,
                    front=player.front,
                    round_bet=player.round_bet,
                    state=StateE(player.state),
                    id=player.id,
                )
                for player in encoded.players
            ],
            position=PositionE(encoded.position),
            round=RoundE(encoded.round),
            flop_dealt=encoded.flop_dealt,
        )

        return poker
