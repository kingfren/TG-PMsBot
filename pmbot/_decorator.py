import asyncio
from re import compile

from telethon import Button
from telethon.events import NewMessage, StopPropagation
from telethon.errors import FloodWaitError

from .helpers import (
    add_user_to_db,
    BANNED_USERS,
    BOT_USERS,
    fsub_checker,
    FSUB_CHANNEL,
    FSUBBED_USERS,
)

from . import bot, Config, LOGS


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def pattern_compiler(pattern, take_args):
    if pattern:
        formt = rf"^[!/]{pattern}(?:@{bot.me.username})?"
        formt += " ?(.*)" if take_args else "$"
        return compile(formt)


def pmbot(pattern, owner_only=False, private=False, **kwargs):
    take_args = kwargs.pop("take_args", 0)
    if "forwards" not in kwargs:
        kwargs["forwards"] = False
    if owner_only:
        kwargs["from_users"] = Config.OWNER_ID

    def _dec(func):
        async def defunc(e):
            user_id = e.sender_id
            if user_id in BANNED_USERS or (bool(private) and not e.is_private):
                return

            asyncio.create_task(add_user_to_db(user_id))
            if Config.FORCE_SUBSCRIBE and e.is_private:
                _is_subbed = await fsub_checker(user_id)
                if not _is_subbed:
                    _message = "**You need to Join this Channel first.** 👇👇"
                    _invite_link = FSUB_CHANNEL()[0][1]
                    _buttons = [
                        [Button.url("Join This Channel 🕛", url=_invite_link)],
                        [Button.inline("Refresh 🔄", data="CB_fsub")],
                    ]
                    await e.reply(_message, buttons=_buttons)
                    return

            try:
                await func(e)
            except FloodWaitError as fw:
                LOGS.error(f"Sleeping for {fw.seconds} seconds..")
                await asyncio.sleep(fw.seconds + 5)
                return
            except StopPropagation:
                raise StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException as exc:
                LOGS.exception(exc)

        pattern = pattern_compiler(pattern, take_args)
        bot.add_event_handler(
            defunc, NewMessage(incoming=True, pattern=pattern, **kwargs)
        )
        return defunc

    return _dec
