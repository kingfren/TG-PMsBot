import asyncio
from collections import deque
from time import time
from re import compile

from telethon.events import NewMessage, StopPropagation
from telethon.errors import FloodWaitError, UserNotParticipantError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.types import Channel, Chat
from telethon.utils import get_display_name

from . import *


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Force Subscribe handler


class Cache:
    sleepTime = 600

    def __init__(
        self,
        maxlen=None,  # max len of cache; None = inf
        auto_clear=None,  # clear cache time in sec; None = no cleanup
    ):
        self.cleaner = auto_clear
        self.data = deque(maxlen=maxlen)
        if self.cleaner:
            self.task = asyncio.create_task(self.handle_cleanups())

    def add_data(self, data):
        if self.cleaner:
            data = (data, time())
        self.data.append(data)

    def __call__(self):
        return self.data

    async def handle_cleanups(self):
        while True:
            await asyncio.sleep(self.sleepTime)
            for data, s_time in self.data:
                if time() - s_time > self.cleaner:
                    try:
                        self.data.remove((data, s_time))
                    except ValueError:
                        pass


FSUBBED_USERS = Cache(maxlen=150, auto_clean=24 * 60 * 60)
FSUB_CHANNEL = Cache(maxlen=1, auto_clean=7200)


async def set_fsub_chat():
    try:
        entity = await bot.get_entity(Config.FORCE_SUBSCRIBE)
        username = getattr(entity, "username", None)
        if username:
            invite_link = f"https://t.me/{username}"
        else:
            if isinstance(ent, Channel):
                full = await bot(GetFullChannelRequest(Config.FORCE_SUBSCRIBE))
            elif isinstance(ent, Chat):
                full = await bot(GetFullChatRequest(Config.FORCE_SUBSCRIBE))
            else:
                raise TypeError("Invalid Chat Type..")
            if full.full_chat.exported_invite:
                invite_link = full.full_chat.exported_invite.link
            else:
                raise TypeError("Invite User Permission Missing")
        FSUB_CHANNEL.add_data((ent, invite_link))
    except Exception:
        LOGS.exception("Error in FORCE_SUBSCRIBE:")


async def fsub_checker(user_id):
    if not FSUB_CHANNEL():
        await set_fsub_chat()
    if user_id == Config.OWNER_ID or user_id in FSUBBED_USERS():
        return True
    try:
        await bot.get_permissions(FSUB_CHANNEL()[0][0], user_id)
        FSUBBED_USERS.add_data(user_id)
        return True
    except UserNotParticipantError:
        return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Decorator handlers


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
            if e.sender_id in BANNED_USERS or (bool(private) and not e.is_private):
                return

            if (
                e.sender_id != Config.OWNER_ID
                and Config.FORCE_SUBSCRIBE
                and e.is_private
            ):
                _is_subbed = await fsub_checker(user_id)
                if not _is_subbed:
                    _message = "**You need to Join this Channel first.** ☠️✨"
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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Helper Functions


def mention(user):
    username = getattr(user, "username", None)
    if username:
        return "@" + username
    fullname = get_display_name(user)
    return f"[{fullname}](tg://user?id={user.id})"


def time_formatter(ms):
    minutes, seconds = divmod(int(ms / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if not tmp:
        return "0s"
    return tmp[:-1] if tmp.endswith(":") else tmp


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# DB Helpers


async def save_msg_id(msg_id, user_id):
    key = "_PMBOT_MESSAGE_IDS"
    value = await redis.get_key(key)
    if value and type(value) is dict:
        value.update({msg_id: user_id})
    else:
        value = {msg_id: user_id}
    await redis.set_key(key, value)


async def get_user_from_msg_id(msg_id):
    key = "_PMBOT_MESSAGE_IDS"
    data = await redis.get_key(key)
    if data:
        return data.get(msg_id)

async def add_user_to_db(user_id):
    key = "_PMBOT_USERS"
    value = await redis.get_key(key)
    if value and type(value) is list:
        value.append(user_id)
    else:
        value = [user_id]
    await redis.set_key(key, value)
