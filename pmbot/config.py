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
    FORCE_SUBSCRIBE = getenv("FORCE_SUBSCRIBE")  # put chat id
    TZ = getenv("TZ", "Asia/Kolkata")  # timezone
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
    LOGS.critical(f"Some Compulsory Vars are Missing:  {', '.join(missing)}")
    quit()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# set timezone
environ["TZ"] = Config.TZ
tzset()

# fsub
fsub = Config.FORCE_SUBSCRIBE
if fsub and fsub[1:].isdigit():
    Config.FORCE_SUBSCRIBE = int(fsub)
