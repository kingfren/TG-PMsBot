from time import time

from ..helpers import time_formatter
from . import Config, pmbot, HELP_STRING


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@pmbot(pattern="ping")
async def ping_bot(e):
    start = time()
    msg = await e.reply("`Pong !!`")
    end = time()
    resp = round((end - start) * 1000)
    uptime = time_formatter((end - Config.STARTUP_TIME) * 1000)
    await msg.edit(
        f"**Pong !!** `{resp}ms` \n**Uptime -** `{uptime}`",
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@pmbot(pattern="help", private=True)
async def helper(e):
    await e.reply(HELP_STRING)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@pmbot(pattern="ids?")
async def get_ids(e):
    if e.is_private:
        await e.reply(f"**User ID:**  `{e.sender_id}`")
        return
    reply = await e.get_reply_message()
    _format = (
        ("Replied User's ID", str(reply.sender_id))
        if reply
        else ("User ID", str(e.sender_id))
    )
    ids_text = "**{}:**  `{}` \n\n".format(*_format)
    ids_text += f"**Chat ID**:  `{e.chat_id}` \n**Message ID:** `{e.id}`"
    await e.reply(ids_text)
