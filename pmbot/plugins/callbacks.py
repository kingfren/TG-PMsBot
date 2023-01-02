from re import compile
from time import time
from platform import python_version

from telethon.events import callbackquery
from telethon import Button, __version__

from ..helpers import mention, time_formatter
from .. import bot, redis, Config, __bot_version__
from . import get_display_name, HELP_STRING, CB_ABOUT_STRING, CB_STAT_STRING, START_BUTTONS, START_STRING


_back_button = [Button.inline("Back 🔙", data="CB_default")]


@bot.on(
    callbackquery.CallbackQuery(
        data=compile("CB_(.*)"),
    )
)
async def callbacks(e):
    cb_data = e.data_match.group(1).decode()

    if cb_data == "help":
        await e.edit(HELP_STRING, buttons=_back_button)

    elif cb_data == "default":
        buttons = START_BUTTONS.copy()
        if e.sender_id == Config.OWNER_ID:
            buttons.append([Button.inline("Stats Of Bot ⌛", data="CB_stats")])
        else:
            buttons.append([Button.inline("Help 📘", data="CB_help")])
        await e.edit(
            START_STRING.format(mention(e.sender)),
            buttons=buttons,
        )

    elif cb_data == "stats":
        allUsers = await redis.get_key("_PMBOT_USERS")
        allMsgIds = await redis.get_key("_PMBOT_MESSAGE_IDS")
        edit_text = CB_STAT_STRING.format(
            time=time_formatter((time() - Config.STARTUP_TIME) * 1000),
            users=str(len(allUsers)),
            total_msg=str(len(allMsgIds)),
        )
        await e.edit(edit_text, buttons=_back_button)

    elif cb_data == "start":
        await e.answer(url=f"https://t.me/{bot.me.username}?start=start")

    elif cb_data == "fsub":
        if not Config.FORCE_SUBSCRIBE:
            return await e.answer()
        is_subbed = await fsub_checker(e.sender_id)
        if not is_subbed:
            res = "You Haven't Joined the Channel Yet. Please Join the Channel and Try Again 🤓"
            await e.answer(res, alert=True)
        else:
            await e.answer("uwu Thanks for Joining !! ✨✨")
            await asyncio.sleep(1.5)
            await e.edit("**__You Can Use this Bot normally Now..__**", buttons=None)

    elif cb_data == "about":
        edit_text = CB_ABOUT_STRING.format(
            my_name=get_display_name(bot.me),
            my_username=bot.me.username,
            my_version=__bot_version__,
            owner=mention(bot.owner),
            python=python_version(),
            telethon=__version__,
            source="https://github.com/libgnu/TG-PMsBot",
        )
        await e.edit(edit_text, buttons=_back_button)
