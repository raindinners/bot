from __future__ import annotations

from contextlib import suppress

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    ChatAdministratorRights,
)

from core.settings import bot_settings


async def set_commands_private_chat(bot: Bot) -> None:
    await bot.set_my_commands(
        commands=[BotCommand(command="/start", description="🖐 Welcome message")],
        scope=BotCommandScopeAllPrivateChats(),
    )


async def set_commands(bot: Bot) -> None:
    await set_commands_private_chat(bot=bot)


async def set_default_administrator_rights(bot: Bot) -> None:
    await bot.set_my_default_administrator_rights(
        rights=ChatAdministratorRights(
            is_anonymous=False,
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_promote_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_post_stories=False,
            can_edit_stories=False,
            can_delete_stories=False,
        ),
    )


async def setup_bot_name(bot: Bot) -> None:
    await bot.set_my_name(name="Pokerlostkiekie")


async def set_short_description(bot: Bot) -> None:
    await bot.set_my_short_description(short_description="Play Poker via me!")


async def setup_bot(bot: Bot) -> None:
    await set_commands(bot=bot)
    await set_default_administrator_rights(bot=bot)
    await setup_bot_name(bot=bot)
    await set_short_description(bot=bot)


async def create_bot() -> Bot:
    bot = Bot(
        token=bot_settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )
    with suppress(TelegramAPIError):
        await setup_bot(bot=bot)

    return bot
