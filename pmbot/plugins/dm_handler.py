from . import bot, Config, pmbot, mention
from ..helpers import MESSAGE_IDS, save_msg_id


pmFunc = lambda e: e.is_private and not e.text.startswith(("/", "!"))


@pmbot(pattern=None, forwards=None, func=pmFunc)
async def pm_forwards(e):
    user_id = e.sender_id
    if user_id != Config.OWNER_ID:
        fwded = await e.forward_to(bot.owner)
        await save_msg_id(fwded.id, user_id)
        if e.fwd_from:
            x = f"**Message Sent by: ** \n\n**User ID:** `{msg.sender_id}` \n**Mention:** {mention(msg.sender)}"
            await fwded.reply(x)

    elif e.is_reply:  # sent by owner
        replied_user = MESSAGE_IDS.get(e.reply_to_msg_id)
        if replied_user:
            await e.client.send_message(replied_user, e.message)
