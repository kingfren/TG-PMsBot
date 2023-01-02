__all__ = ["bot", "Config", "redis", "LOGS"]

__bot_version__ = "3.5.5"


from telethon import TelegramClient

from .logger import LOGS
from .config import Config
from .database import DataBase


try:
    bot = TelegramClient(
        None, Config.API_ID, Config.API_HASH, flood_sleep_threshold=300
    )
except Exception as exc:
    LOGS.exception(exc)
    LOGS.critical("Error While Starting Telethon")
    quit()

redis = DataBase()
