from . import Button, mention, pmbot, Config, START_BUTTONS, START_STRING


@pmbot(pattern="start", take_args=True)
async def start(e):
    if not e.is_private:
        buttons = [Button.inline("Try Now ⭐", data="CB_start")]
    else:
        buttons = START_BUTTONS.copy()
        if e.sender_id == Config.OWNER_ID:
            buttons.append([Button.inline("Stats Of Bot ⌛", data="CB_stats")])
        else:
            buttons.append([Button.inline("Help 📘", data="CB_help")])

    await e.reply(
        START_STRING.format(mention(e.sender)), buttons=buttons,
    )
