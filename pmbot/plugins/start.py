from telethon import Button

from . import mention, pmbot, bot, Config, START_BUTTONS, START_STRING


@pmbot(pattern="start", take_args=True)
async def start(e):
    if not e.is_private:
        url = f"https://t.me/{bot.me.username}?start=something"
        buttons = [Button.inline("Try Now ⭐", url=url)]
    else:
        buttons = START_BUTTONS.copy()
        if e.sender_id == Config.OWNER_ID:
            button.append([Button.inline("Stats Of Bot ⌛", data="CB_stats")])
        else:
            button.append([Button.inline("Help 📘", data="CB_help")])

    await e.reply(
        START_STRING.format(mention(e.sender)),
        buttons=button,
    )
