import asyncio
from pathlib import Path
from importlib import import_module

from . import *
from . import BANNED_USERS
from .helper import set_fsub_chat


def load_plugins():
    path = Path() / "pmbot" / "plugins"
    LOGS.info(f"Loading Plugins from {path}")
    allFiles = (
        i for i in path.glob("*.py") if i.is_file() and not i.name.startswith("__")
    )
    for file in allFiles:
        try:
            plug = str(file).replace(".py", "").replace("/", ".")
            import_module(plug)
            LOGS.info(f"Loaded Plugin - {file.name}")
        except BaseException:
            LOGS.exception(f"Error in Loading Plugin - {file.name}")


async def get_owner():
    try:
        LOGS.info(f"Checking - OWNER_ID ...")
        bot.owner = await bot.get_entity(Config.OWNER_ID)
    except Exception:
        LOGS.exception()
        LOGS.critical("Master, Please /start the bot Once 👀")
        quit()


async def update_banned_users():
    banned = await redis.get_key("_PMBOT_BANNED_USERS")
    if banned and type(banned) == set:
        BANNED_USERS |= banned
        await redis.set_key("_PMBOT_BANNED_USERS", BANNED_USERS)
    else:
        await redis.del_key("_PMBOT_BANNED_USERS")


async def startup_func():
    await get_owner()
    await update_banned_users()
    await set_fsub_chat()


async def main():
    try:
        LOGS.info("Trying to Login with Bot..")
        await bot.start(bot_token=Config.BOT_TOKEN)
    except BaseException:
        LOGS.exception()
        LOGS.critical("Error while Connecting to Telegram.")
        quit()

    # get_me
    await asyncio.sleep(1)
    bot.me = await bot.get_me()
    LOGS.info(f"Logged in Successfully as @{bot.me.username}")

    # Redis DB
    redis.finish_setup(Config.REDIS_URI, Config.REDIS_PASSWORD)
    await startup_func()
    load_plugins()
    LOG.info("Bot is Running!")


try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

loop.run_until_complete(main())
bot.run_until_disconnected()
