from __future__ import annotations

from contextlib import suppress
from typing import List, Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from pokerengine.enums import PositionE, RoundE
from pokerengine.pokerengine_core.engine import PlayerAction
from pokerengine.pokerengine_core.enums.action import ActionE

from enums import Position, Round
from keyboards import (
    actions_inline_keyboard_builder,
    information_inline_keyboard_builder,
    player_cards_inline_keyboard_builder,
)
from logger import logger
from poker import Poker
from schemas import Action, ApplicationSchema, Card, Player, PokerCards, Traits


class Information(ApplicationSchema):
    traits: Traits
    round: Round
    players: Player
    current: Position
    poker_cards: PokerCards
    flop_dealt: bool
    pot: int
    pot_rake: int
    actions: Optional[List[Action]] = None
    players: List[Player]


def find_check_or_fold(actions: List[PlayerAction]) -> PlayerAction:
    for action in actions:
        if action.action == ActionE.CHECK:
            return action
        if action.action == ActionE.FOLD:
            return action

    return PlayerAction(amount=0, action=ActionE.NONE, position=PositionE.NONE)


async def send_game_information(bot: Bot, inline_message_id: str, poker: Poker) -> None:
    information = Information(
        traits=Traits.model_validate(poker.engine.traits),
        round=poker.engine.round.round.value,
        flop_dealt=poker.engine.round.flop_dealt,
        players=[Player.model_validate(player) for player in poker.engine.players.players],
        current=poker.engine.positions.current.value,
        poker_cards=PokerCards(
            board=[
                Card(value=card.card, string=str(card))
                for card in poker.cards.board[
                    : (
                        poker.engine.round.round.value + 2
                        if poker.engine.round.round != RoundE.PREFLOP
                        else RoundE.PREFLOP.value
                    )
                ]
            ],
        ),
        pot=poker.engine.pot.pot(),
        pot_rake=poker.engine.pot.pot_rake(),
        actions=[Action.model_validate(action) for action in poker.engine.actions.actions],
    )

    if poker.preview_round != poker.engine.round.round.value:
        poker.preview_round = poker.engine.round.round.value

        _current_player_id, current_player_name = poker.engine.positions.player.id.split("_")
        with suppress(TelegramBadRequest):
            await bot.edit_message_text(
                text=(
                    f"Traits: {information.traits.sb_bet} SB "
                    f"| {information.traits.bb_bet} BB "
                    f"| {information.traits.min_raise} MR"
                    f"\n\n"
                    f"Round: {Round(information.round).as_string()}"
                    f"\n\n"
                    f"Board: {(' '.join(card.string.upper().replace('C', '♣️').replace('D', '♦️').replace('H', '♥️').replace('S', '♠️') for card in information.poker_cards.board) if information.poker_cards.board else 'There is no board cards now')}"
                    f"\n\n"
                    f"Players in the game: {len(information.players)}"
                    f"\n"
                    f"Current: {current_player_name}"
                    f"\n\n"
                    f"Pot: {information.pot}"
                ),
                inline_message_id=inline_message_id,
            )

        with suppress(TelegramBadRequest):
            await bot.edit_message_reply_markup(
                inline_message_id=inline_message_id,
                reply_markup=player_cards_inline_keyboard_builder(
                    inline_message_id=inline_message_id
                )
                .attach(information_inline_keyboard_builder(inline_message_id=inline_message_id))
                .attach(
                    actions_inline_keyboard_builder(
                        inline_message_id=inline_message_id, actions=information.actions
                    )
                )
                .as_markup(),
            )


async def information(bot: Bot, inline_message_id: str, poker: Poker) -> None:
    if not poker.started or poker.engine.round.terminal_state:
        return logger.debug("Skipping auto action: wrong game state")

    await send_game_information(bot=bot, inline_message_id=inline_message_id, poker=poker)

    return None
