import logging
import os
from io import StringIO
from pathlib import Path

from dotenv import load_dotenv
from interactions import MISSING

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

ENV_PATH = Path.cwd().parent / ".env"

BOT_TOKEN = None
BOT_SCOPE = None

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

try:
    if not (BOT_TOKEN := os.environ.get("BOT_TOKEN")):
        BOT_TOKEN = None
    if not (BOT_SCOPE := int(os.environ.get("BOT_SCOPE"))):
        BOT_SCOPE = MISSING
    else:
        logger.info(f"Bot scope set to server ID {BOT_SCOPE}")
except TypeError:
    pass
if BOT_TOKEN is None:
    raise ValueError("No BOT_TOKEN provided!")

