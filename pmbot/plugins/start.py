from telethon import Button

from . import mention, pmbot, bot, Config, START_BUTTONS, START_STRING, add_user_to_db


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@pmbot(pattern="start", take_args=True)
async def start(e):
    _mention = mention(e.sender)
    buttons = START_BUTTONS.copy()
    if not e.is_private:
        url = f"https://t.me/{bot.me.username}?start=something"
        buttons.append([Button.inline("Try Now ⭐", url=url)])
    else:
        asyncio.create_task(add_user_to_db(e.sender_id))
        if e.sender_id == Config.OWNER_ID:
            button.append([Button.inline("Stats Of Bot ⌛", data="CB_stats")])
        else:
            button.append([Button.inline("Help 📘", data="CB_help")])

    await e.reply(
        START_STRING.format(_mention),
        buttons=button,
    )
