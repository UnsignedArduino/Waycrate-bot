import logging
import os
from io import StringIO
from pathlib import Path

from dotenv import load_dotenv
from interactions import MISSING

from utils.english import boolean_parse, time_parse
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

ENV_PATH = Path.cwd().parent / ".env"

BOT_TOKEN = None
BOT_SCOPE = None
GET_REAL_DATA = True
REFRESH_RATE_SECS = None

if not ENV_PATH.exists():
    raise FileNotFoundError(f"Path to .env file "
                            f"({ENV_PATH.expanduser().resolve()}) does not "
                            f"exist!")

logger.info(f"Loading .env from {ENV_PATH.expanduser().resolve()}")

env_text = "\n".join((
    line for line in ENV_PATH.read_text().replace("\r", "").split("\n")
    if not line.startswith("//")
))

load_dotenv(stream=StringIO(env_text))

if not (BOT_TOKEN := os.environ.get("BOT_TOKEN")):
    raise ValueError("No BOT_TOKEN provided!")

try:
    if not (BOT_SCOPE := int(os.environ.get("BOT_SCOPE"))):
        BOT_SCOPE = MISSING
    else:
        logger.info(f"Bot scope set to server ID {BOT_SCOPE}")
except TypeError:
    pass

GET_REAL_DATA = boolean_parse(os.environ.get("GET_REAL_DATA"))

if GET_REAL_DATA:
    logger.info("Using real data from GitHub API for emulated filesystem")
else:
    logger.warning("Using fake data for emulated filesystem")

REFRESH_RATE_SECS = time_parse(os.environ.get("DATA_REFRESH_RATE"))

logger.info(f"Refresh will be triggered on command if {REFRESH_RATE_SECS} "
            f"has passed since the last call!")
