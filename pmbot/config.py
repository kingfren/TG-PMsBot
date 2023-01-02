__all__ = ["Config"]

from os import environ, getenv
from time import time, tzset

from dotenv import load_dotenv, find_dotenv

from .logger import LOGS


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Check .env.sample for example
load_dotenv(find_dotenv())

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Configs:
    # compulsory variables.
    API_ID = int(getenv("API_ID"))
    API_HASH = getenv("API_HASH")
    BOT_TOKEN = getenv("BOT_TOKEN")
    REDIS_URI = getenv("REDIS_URI")
    REDIS_PASSWORD = getenv("REDIS_PASSWORD")
    OWNER_ID = int(getenv("OWNER_ID"))

    # optional variables.
    FORCE_SUBSCRIBE = getenv("FORCE_SUBSCRIBE")
    SUDO_USERS = getenv("SUDO_USERS")
    TIMEZONE = getenv("TZ", "Asia/Kolkata")
    STARTUP_TIME = time()  # automatic


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Config = Configs()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

imp_vars = (
    "API_ID",
    "API_HASH",
    "BOT_TOKEN",
    "REDIS_URI",
    "REDIS_PASSWORD",
    "OWNER_ID",
)
missing = list(filter(getattr(Config, key, None), imp_vars))
if missing:
    LOGS.critical(f"Missing Vars:  {', '.join(missing)}")
    quit()

sudos = Config.SUDO_USERS
fsub = Config.FORCE_SUBSCRIBE
environ["TZ"] = Config.TIMEZONE
tzset()

if sudos:
    Config.SUDO_USERS = tuple(int(x) for x in sudos.split())
if fsub:
    try:
        Config.FORCE_SUBSCRIBE = int(fsub)
    except ValueError:
        pass
