__all__ = ["LOGS"]

import logging
import platform

from . import __bot_version__

# -----------------------------------------------------------------


def fix_logging():
    handler = logging.FileHandler
    handler._builtin_open = open

    def _new_open(self):
        open_func = self._builtin_open
        return open_func(self.baseFilename, self.mode)

    setattr(handler, "_open", _new_open)


if int(platform.python_version_tuple()[1]) < 10:
    fix_logging()

# -----------------------------------------------------------------

LOGS = logging.getLogger("PM-Bot")
format = logging.Formatter(
    "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
    datefmt="%d/%m, %H:%M:%S",
)

# -----------------------------------------------------------------

logging.basicConfig(
    format=format,
    level=logging.DEBUG,
    datefmt="%d/%m, %H:%M:%S",
    handlers=[
        logging.FileHandler("logs.txt", mode="w+"),
        logging.StreamHandler(),
    ],
)

LOGS.info(f"Starting PMBot! - {__bot_version__}")
