from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple, Union

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.formatting import Bold, Text, as_list, as_section
from aiogram.utils.text_decorations import markdown_decoration
from pokerengine import schema
from pokerengine.engine import EngineRake01, Player
from pokerengine.enums import Action, Round
from pokerengine.pretty_string import PrettyCard

from callback_data import (
    ActionsCallbackData,
    CardsCallbackData,
    PinCallbackData,
    SelectActionCallbackData,
)
from core.poker.schema import Poker


class Messages:
    def __init__(
        self,
        bot: Bot,
        pretty_card: Optional[PrettyCard] = None,
        poker_id: Optional[str] = None,
        inline_message_id: Optional[str] = None,
        player: Optional[Player] = None,
    ) -> None:
        self.bot = bot
        self.poker_id = poker_id
        self.pretty_card = pretty_card
        self.inline_message_id = inline_message_id
        self.player = player

    async def send_actions_state(
        self, engine: EngineRake01, selected_action: Dict[str, Any]
    ) -> None:
        await self.bot.edit_message_text(
            **as_section(
                Bold("Actions"),
                Text(
                    f"Selected: {(Action(selected_action['action']).name.capitalize() + ', ' + str(selected_action['amount'])) if selected_action is not None else 'No action selected'}"
                ),
            ).as_kwargs(),
            chat_id=str(engine.current_player.parameters["chat_id"]),
            message_id=int(engine.current_player.parameters["message_id"]),  # noqa
        )

    async def send_actions_state_keyboard(self, engine: EngineRake01) -> None:
        await self.bot.edit_message_reply_markup(
            chat_id=str(engine.current_player.parameters["chat_id"]),
            message_id=int(engine.current_player.parameters["message_id"]),  # noqa
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    *[
                        [
                            InlineKeyboardButton(
                                text=f"{action.action.name.capitalize()}, max bet: {action.amount}",
                                callback_data=SelectActionCallbackData(
                                    action=action.action.value,
                                    position=action.position.value,
                                    amount=action.amount,
                                ).pack(),
                            )
                        ]
                        for action in engine.possible_actions
                    ],
                    [
                        InlineKeyboardButton(
                            text="Done", callback_data=ActionsCallbackData(is_done=True).pack()
                        )
                    ],
                ]
            ),
        )

    async def send_join(self) -> None:
        await self.bot.edit_message_text(
            **Text("Poker created, push down button to join.").as_kwargs(),
            inline_message_id=self.inline_message_id,
        )

    async def send_join_keyboard(self) -> None:
        await self.bot.edit_message_reply_markup(
            inline_message_id=self.inline_message_id,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Join",
                            url=await create_start_link(bot=self.bot, payload=self.poker_id),
                        )
                    ]
                ]
            ),
        )

    async def send_loading_state_broadcast(
        self,
        players: List[schema.Player],
        is_stopped: bool = False,
        start_at: Optional[float] = None,
    ) -> None:
        for player in players:
            await self.bot.edit_message_text(
                **(
                    Bold("Poker stopped.").as_kwargs()
                    if is_stopped
                    else Bold(
                        f"Poker starts in {int(start_at - time.time())} seconds."
                    ).as_kwargs()
                ),
                chat_id=str(player.parameters["chat_id"]),
                message_id=int(player.parameters["message_id"]),  # noqa
            )

    async def send_main_state(
        self, poker: Poker, engine: EngineRake01, cards: schema.Cards
    ) -> None:
        await self.bot.edit_message_text(
            **as_list(
                as_section(Bold("Round"), Text(engine.round.name.capitalize())),
                as_section(
                    Bold("Bets"),
                    Text(f"Max: {Bold(engine.highest_bet).as_markdown()}"),
                    "\n",
                    Text(f"Total bets: {Bold(engine.pot).as_markdown()}"),
                ),
                as_section(
                    Bold("Players"),
                    as_list(
                        Bold(
                            markdown_decoration.quote(
                                f"Current: {engine.current_player.parameters.get('name')}"
                            )
                        ),
                        Bold(
                            markdown_decoration.quote(
                                f"Auto action will execute in {int(poker.auto_action_time - time.time())} seconds"
                                if poker.auto_action_time
                                else "No auto action present"
                            )
                        ),
                    ),
                    "\n\n",
                    as_section(
                        "All players",
                        as_list(
                            *[
                                Text(
                                    markdown_decoration.quote(
                                        f"Name: {player.parameters.get('name')},"
                                        f" stack: {player.stack},"
                                        f" bet: {player.bet},"
                                        f" round_bet: {player.round_bet},"
                                        f" state: {player.state.name.lower()}"
                                    )
                                )
                                for player in engine.players
                            ]
                        ),
                    ),
                ),
                as_section(
                    Bold("Board"),
                    as_list(
                        *(
                            [
                                Text(self.pretty_card.as_pretty_string(value=card))
                                for card in cards.board[
                                    : (
                                        engine.round.value + 2
                                        if engine.round != Round.PREFLOP
                                        else Round.PREFLOP.value
                                    )
                                ]
                            ]
                            or [Text("Currently not present")]
                        ),
                        sep=" ",
                    ),
                ),
                sep="\n\n",
            ).as_kwargs(replace_parse_mode=False),
            chat_id=str(self.player.parameters["chat_id"]),
            message_id=int(self.player.parameters["message_id"]),  # noqa
        )

    async def send_main_state_keyboard(self, player: Optional[Player] = None) -> None:
        player = self.player if not player else player
        await self.bot.edit_message_reply_markup(
            chat_id=str(self.player.parameters["chat_id"]),
            message_id=int(self.player.parameters["message_id"]),  # noqa
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Actions", callback_data=ActionsCallbackData().pack()
                        )
                    ],
                    [InlineKeyboardButton(text="Cards", callback_data=CardsCallbackData().pack())],
                ]
            ),
        )

    async def send_pin_state(self, engine: EngineRake01) -> None:
        await self.bot.edit_message_text(
            **Text("Enter amount").as_kwargs(),
            chat_id=str(engine.current_player.parameters["chat_id"]),
            message_id=int(engine.current_player.parameters["message_id"]),  # noqa
        )

    async def send_pin_state_keyboard(self, engine: EngineRake01) -> None:
        await self.bot.edit_message_reply_markup(
            chat_id=str(engine.current_player.parameters["chat_id"]),
            message_id=int(engine.current_player.parameters["message_id"]),  # noqa
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="1",
                            callback_data=PinCallbackData(action="add", argument="1").pack(),
                        ),
                        InlineKeyboardButton(
                            text="2",
                            callback_data=PinCallbackData(action="add", argument="2").pack(),
                        ),
                        InlineKeyboardButton(
                            text="3",
                            callback_data=PinCallbackData(action="add", argument="3").pack(),
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="4",
                            callback_data=PinCallbackData(action="add", argument="4").pack(),
                        ),
                        InlineKeyboardButton(
                            text="5",
                            callback_data=PinCallbackData(action="add", argument="5").pack(),
                        ),
                        InlineKeyboardButton(
                            text="6",
                            callback_data=PinCallbackData(action="add", argument="6").pack(),
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="7",
                            callback_data=PinCallbackData(action="add", argument="7").pack(),
                        ),
                        InlineKeyboardButton(
                            text="8",
                            callback_data=PinCallbackData(action="add", argument="8").pack(),
                        ),
                        InlineKeyboardButton(
                            text="9",
                            callback_data=PinCallbackData(action="add", argument="9").pack(),
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="<", callback_data=PinCallbackData(action="remove").pack()
                        ),
                        InlineKeyboardButton(
                            text="0",
                            callback_data=PinCallbackData(action="add", argument="0").pack(),
                        ),
                        InlineKeyboardButton(
                            text="=", callback_data=PinCallbackData(action="apply").pack()
                        ),
                    ],
                ]
            ),
        )

    async def send_winners_broadcast(
        self, poker: Poker, response: Union[List[Tuple[str, int]], List[int]]
    ) -> None:
        texts = []
        for index, chips in enumerate(response):
            if isinstance(chips, Tuple):
                result, chips = chips
            else:
                result, chips = "all exited", chips
            if chips > 0:
                result = "won by " + result
            else:
                result = "lose by " + result

            player = poker.engine.players[index]  # noqa
            texts.append(
                Text(
                    markdown_decoration.quote(
                        f"Player {player.parameters.get('name')} got {chips} chips and {result}"
                    )
                )
            )

        engine = poker.engine.to_original()
        for player in poker.engine.players:
            await self.bot.edit_message_text(
                **as_list(
                    *texts,
                    "\n",
                    as_section(
                        Bold("Board"),
                        as_list(
                            *(
                                [
                                    Text(self.pretty_card.as_pretty_string(value=card))
                                    for card in poker.cards.board[
                                        : (
                                            engine.round.value + 2
                                            if engine.round != Round.PREFLOP
                                            else Round.PREFLOP.value
                                        )
                                    ]
                                ]
                                or [Text("Currently not present")]
                            ),
                            sep=" ",
                        ),
                    ),
                ).as_kwargs(replace_parse_mode=False),
                chat_id=str(player.parameters["chat_id"]),
                message_id=int(player.parameters["message_id"]),  # noqa
            )

    async def send_winners_keyboard_broadcast(self, poker: Poker) -> None:
        for player in poker.engine.players:
            await self.bot.edit_message_reply_markup(
                chat_id=str(player.parameters["chat_id"]),
                message_id=int(player.parameters["message_id"]),  # noqa
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="Cards", callback_data=CardsCallbackData().pack()
                            )
                        ],
                    ]
                ),
            )
