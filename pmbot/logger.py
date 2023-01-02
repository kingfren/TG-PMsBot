import logging
import platform

import coloredlogs

from . import __bot_version__


# -----------------------------------------------------------------


if int(platform.python_version_tuple()[1]) < 10:
    handler = logging.FileHandler
    handler._builtin_open = open
    _new_open = lambda self: self._builtin_open(self.baseFilename, self.mode)
    setattr(handler, "_open", _new_open)

# ----------------------------------------------------------------------------

LOGS = logging.getLogger("PMBot")
format = "%(asctime)s - %(name)s [%(levelname)s] : %(message)s"

# ----------------------------------------------------------------------------

logging.basicConfig(
    format=format,
    level=logging.INFO,
    datefmt="%d/%m, %H:%M:%S",
    handlers=[
        logging.FileHandler("logs.txt", mode="w+"),
        logging.StreamHandler(),
    ],
)

coloredlogs.install(level=None, logger=LOGS, fmt=format)

# ----------------------------------------------------------------------------

LOGS.info("Starting PMBot!")
LOGS.info(f"Bot Version - {__bot_version__}")
LOGS.info(f"Python Version - {platform.python_version()}")
