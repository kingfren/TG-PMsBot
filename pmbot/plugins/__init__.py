from telethon import Button

from pmbot import *
from pmbot.helpers import mention, get_display_name
from pmbot._decorator import pmbot


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Strings and Buttons

USER_INFO_STR = """
**Full Name:**  `{name}`
**User ID:**  `{id}`
**Mention:**  {mention}
**Is Banned:**  `{banned}`
"""

BROADCAST_STR = """
**Broadcasting to {total} Users ✨**

**Success:** `{success}`
**Fail:** `{failed}`
**ETA:** `{eta}`
"""

HELP_STRING = """
**•• All Commands of this Bot ••**

/help - Get this text again.
/start - Check if bot is Alive and Running.
/ping - Check Latency.
/id - Get User/Chat ID.
/logs - (owner) - Get Bot Logs.
/info - (owner) - Get User Info.
/block - (owner) - Block the User from using Bot.
/unblock - (owner) - Unblock User.
/broadcast - (owner) - Broadcast a Message to all Bot Users.
/listblocked - (owner) - List Blocked Users of Bot.

~ __'/' and '!' can be Used as Handlers__
~ __Commands with owner tag, Can only be used by my Owner__
"""

START_STRING = """
**Hello** {} !! 👋

**All of your Messages will be Forwarded to my Owner**
🤓
"""

START_BUTTONS = [
    [
        Button.url("About 📚", data="CB_about"),
        Button.inline("Help 📡", data="CB_help"),
    ]
]

CB_STAT_STRING = """
• I'm Online Since {time}

• Currently, I have {users} Users in My Database."

• I have Forwarded you total of {total_msg} messages in my Lifetime 🤓
"""

CB_ABOUT_STRING = """
**This is Just a PMBot. I can help in Managing PM easily.
Send me any message I will forward it to my Owner.**

🤖 **Bot's Name:**  [{my_name}](https://t.me/{my_username})

⭐ **Bot's Owner:**  {owner}

🔄 **Source Code:**  [{my_version}]({source})

📝 **Language:**  [Python {python}](https://www.python.org)

📚 **Library:**  [Telethon {telethon}](https://docs.pyrogram.org)

‍💻 **Developer:**  [@libgnu](https://telegram.dog/spemgod)
"""

