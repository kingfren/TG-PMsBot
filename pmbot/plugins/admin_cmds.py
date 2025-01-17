import asyncio
from os import remove

from ..helpers import time_formatter, MESSAGE_IDS, BANNED_USERS
from . import (
    get_display_name,
    LOGS,
    mention,
    pmbot,
    redis,
    USER_INFO_STR,
    BROADCAST_STR,
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@pmbot(pattern="logs", owner_only=True)
async def send_logs(e):
    x = await e.reply("`Sending Logs..`")
    await e.respond("**PM-Bot LOGS!**", file="logs.txt")
    await x.delete()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@pmbot(pattern="info", owner_only=True, private=True)
async def get_info(e):
    if not e.is_reply:
        await e.reply("`Reply to anyone's Message to get his Info..`")
        return

    my_msg = await e.reply("`Getting Info for this user..`")
    user_id = MESSAGE_IDS.get(e.reply_to_msg_id)
    if not user_id:
        await my_msg.edit("`Could not Found User associated with this Message..`")
        return

    try:
        entity = await e.client.get_entity(user_id)
    except ValueError as exc:
        LOGS.exception(exc)
        await my_msg.edit(f"**ERROR:**  `{exc}`")
        return

    photo = await e.client.download_profile_photo(entity)
    format_msg = USER_INFO_STR.format(
        name=get_display_name(entity),
        id=str(entity.id),
        mention=mention(entity),
        banned=str(entity.id in BANNED_USERS),
    )

    if photo:
        await asyncio.gather(
            e.client.send_message(
                e.chat_id, format_msg, file=photo, reply_to=e.reply_to_msg_id
            ),
            my_msg.delete(),
        )
        remove(photo)
    else:
        await my_msg.edit(format_msg)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@pmbot(pattern="ban", owner_only=True, take_args=True, private=True)
@pmbot(pattern="block", owner_only=True, take_args=True, private=True)
async def ban_users(e):
    global BANNED_USERS
    args = e.pattern_match.group(1)
    reply = e.reply_to_msg_id
    if not reply and not args:
        msg = "Use Like: \n • /ban user_id \n • OR reply /ban to Message of that User."
        return await e.reply(msg)

    key = ""
    if args:
        if not args.isdigit():
            await e.reply("`Pass ID of User to ban`")
            return
        to_ban = int(args)
    else:
        to_ban = MESSAGE_IDS.get(reply)
        if not to_ban:
            await e.reply("`Could not Found User associated with this Message..`")
            return

    if to_ban in BANNED_USERS:
        return await e.reply("__This User is Already Banned..__ 💪")
    BANNED_USERS.add(to_ban)
    await redis.set_key(key, BANNED_USERS)
    await e.reply(f"**Successfully Banned -** `{to_ban}`")


@pmbot(pattern="unban", owner_only=True, take_args=True, private=True)
@pmbot(pattern="unblock", owner_only=True, take_args=True, private=True)
async def unban_users(e):
    global BANNED_USERS
    args = e.pattern_match.group(1)
    reply = e.reply_to_msg_id
    if not reply and not args:
        msg = "Use Like: \n • /unban user_id \n • OR reply /unban to Message of that User."
        return await e.reply(msg)

    key = ""
    if args:
        if not args.isdigit():
            await e.reply("`Pass ID of User to Unban`")
            return
        to_unban = int(args)
    else:
        to_unban = MESSAGE_IDS.get(reply)
        if not to_unban:
            await e.reply("`Could not Found User associated with this Message..`")
            return

    if to_unban not in BANNED_USERS:
        return await e.reply(f"User `{to_unban}` was never Banned.. 🚫")
    BANNED_USERS.remove(to_unban)
    await redis.set_key(key, BANNED_USERS)
    await e.reply(f"**Successfully UnBanned -** `{to_unban}`")


@pmbot(pattern="listbanned", owner_only=True, private=True)
@pmbot(pattern="listblocked", owner_only=True, private=True)
async def list_banned_users(e):
    if not BANNED_USERS:
        return await e.reply("`No Users Have Been Blocked yet..`")
    text = "** • List of Banned Users •**\n"
    for user_id in BANNED_USERS:
        text += f"- `{user_id}`\n"
    await e.reply(text)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@pmbot(pattern="broadcast", owner_only=True)
async def broad_cast(e):
    sleep_time = 5
    if not e.is_reply:
        await e.reply("`Reply to the Message You want to Broadcast..`")
        return

    to_send = await e.get_reply_message()
    my_msg = await to_send.reply("`Please Wait..`")
    allUsers = await redis.get_key("_PMBOT_USERS")
    if not allUsers:
        await my_msg.edit("`No Users in My Database..` ☠️")
        return

    success, failed = 0, 0
    for user_id in allUsers:
        try:
            await asyncio.sleep(sleep_time)
            await e.client.send_message(user_id, to_send)
            success += 1
        except Exception:
            LOGS.error(f"Failed to Broadcast Message at {user_id}")
            failed += 1
        else:
            left_users = len(allUsers) - (success + failed)
            eta = time_formatter((left_users * sleep_time) * 1000)
            edit_text = BROADCAST_STR.format(
                total=str(len(allUsers)),
                success=str(success),
                failed=str(failed),
                eta=eta,
            )
            await my_msg.edit(edit_text)

    await asyncio.sleep(2)
    edit_msg = f"**Successfully Broadcasted this Message to {success} Users.** ✨✨"
    if failed:
        edit_msg += (
            f"\n**Failed in {failed} Users** \n\n__failed chats are saved in logs__"
        )
    await my_msg.edit(edit_msg)
