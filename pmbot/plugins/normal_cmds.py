from time import time

from ..helpers import time_formatter
from . import Config, pmbot, HELP_STRING


@pmbot(pattern="ping")
async def ping_bot(e):
    start_time = time()
    msg = await e.reply("`Pong !!`")
    end_time = time()
    resp = round((end_time - start_time) * 1000)
    uptime = time_formatter((end_time - Config.STARTUP_TIME) * 1000)
    await msg.edit(
        f"**Pong !!** `{resp}ms` \n**Uptime -** `{uptime}`",
    )


@pmbot(pattern="help", private=True)
async def helper(e):
    await e.reply(HELP_STRING)


@pmbot(pattern="ids?")
async def get_ids(e):
    if e.is_private:
        await e.reply(f"**User ID:**  `{e.sender_id}`")
        return
    reply = await e.get_reply_message()
    _format_txt = (
        ("Replied User's ID", str(reply.sender_id))
        if reply
        else ("User ID", str(e.sender_id))
    )
    ids_text = "**{}:**  `{}` \n\n".format(*_format_txt)
    ids_text += f"**Chat ID**:  `{e.chat_id}` \n**Message ID:** `{e.id}`"
    await e.reply(ids_text)
