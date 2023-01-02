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
✨ **Broadcasting this Message to {total} Users..**

✅ **Success:** `{success}`
🚫 **Fail:** `{failed}`
⌛ **ETA:** `{eta}`
"""

HELP_STRING = """
**•• All Commands of this Bot ••**

/help - Get this text again.
/start - Check whether Bot is Running.
/ping - Check Latency.
/id - Get User/Chat ID.
/logs - (owner) - Get Bot Logs.
/info - (owner) - Get User Info.
/unblock - (owner) - Unblock User.
/block - (owner) - Block User from using Bot.
/broadcast - (owner) - Broadcast a Message to all Bot Users.
/listblocked - (owner) - List Blocked Users of Bot.

~ __'/' and '!' can be used as handlers..__
~ __Commands with owner tag, can only be used by Owner.__
"""

START_STRING = """
**Hello,** {} ✨👋✨

**Send me a Message and I will Forward it to my Master.** 🐥
"""

START_BUTTONS = [
    [
        Button.inline("About 📚", data="CB_about"),
        Button.inline("Help 📡", data="CB_help"),
    ]
]

CB_STAT_STRING = """
**• I'm Online Since {time}

• Currently, I have** `{users}` **Users in My Database.** ⭐

__• I have Forwarded {total_msg} messages so far.__ ⭐
"""

CB_ABOUT_STRING = """
**This is Just a PMBot. I can help in Managing DM's.
Send me any message I will forward it to my Owner.**

🤖 **Bot's Name:**  [{my_name}](https://t.me/{my_username})

⭐ **Bot's Owner:**  {owner}

🔄 **Source Code:**  [{my_version}]({source})

📝 **Language:**  [Python v{python}](https://docs.python.org/3)

📚 **Library:**  [Telethon v{telethon}](https://docs.telethon.dev)

‍💻 **Developer:**  [@libgnu](https://telegram.dog/spemgod)
"""
