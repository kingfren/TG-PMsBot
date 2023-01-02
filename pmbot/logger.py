import logging
import platform

from . import __bot_version__

# -----------------------------------------------------------------

if int(platform.python_version_tuple()[1]) < 10:
    handler = logging.FileHandler
    handler._builtin_open = open
    _new_open = lambda self: self._builtin_open(self.baseFilename, self.mode)
    setattr(handler, "_open", _new_open)

# ----------------------------------------------------------------------------

LOGS = logging.getLogger("PMBot")
_format = "%(asctime)s - %(name)s - [%(levelname)s] - %(filename)s – %(message)s"
format = logging.Formatter(_format, datefmt="%d/%m, %H:%M:%S")

# ----------------------------------------------------------------------------

logging.basicConfig(
    format=format,
    level=logging.DEBUG,
    datefmt="%d/%m, %H:%M:%S",
    handlers=[
        logging.FileHandler("logs.txt", mode="w+"),
        logging.StreamHandler(),
    ],
)

coloredlogs.install(level=None, logger=LOGS, fmt=_format)

# ----------------------------------------------------------------------------

LOGS.info("Starting PMBot!")
LOGS.info(f"Bot Version - {__bot_version__}")
LOGS.info(f"Python Version - {platform.python_version()}")
