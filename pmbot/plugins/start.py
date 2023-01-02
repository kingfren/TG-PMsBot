from . import Button, mention, pmbot, Config, START_BUTTONS, START_STRING


@pmbot(pattern="start", take_args=True)
async def start(e):
    if not e.is_private:
        text = "Hello, {mention(e.sender)} ✨👋✨"
        buttons = [Button.inline("Start in PM ⭐", data="CB_start")]
    else:
        buttons = START_BUTTONS.copy()
        text = START_STRING.format(mention(e.sender))
        if e.sender_id == Config.OWNER_ID:
            buttons.append([Button.inline("Stats Of Bot ⌛", data="CB_stats")])
        else:
            buttons.append([Button.inline("Help 📘", data="CB_help")])

    await e.reply(text, buttons=buttons)
