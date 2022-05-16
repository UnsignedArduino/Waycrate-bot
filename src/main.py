import logging
import os
from io import StringIO
from pathlib import Path

import interactions
from dotenv import load_dotenv
from interactions import MISSING

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

ENV_PATH = Path.cwd().parent / ".env"
COGS_PATH = Path.cwd() / "cogs"

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

BOT_TOKEN = None
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

client = interactions.Client(
    token=BOT_TOKEN,
    presence=interactions.ClientPresence(
        activities=[
            interactions.PresenceActivity(
                type=interactions.PresenceActivityType.WATCHING,
                name="over the Waycrate Discord"
            )
        ],
        status=interactions.StatusType.ONLINE
    ),
    disable_sync=False  # Set disable_sync to True when not editing your
    # commands (name, description, options, etc.)
)


@client.event
async def on_ready():
    logger.info("Ready!")


cogs = [
    module[:-3] for module in COGS_PATH.rglob("*")
    if module.name not in ("__init__.py",) and
       module.suffix == ".py" and
       not module.name.startswith("_")
]

logger.info(f"Importing {len(cogs)} cog{'s' if len(cogs) != 1 else ''}")

for cog in cogs:
    cog_name = "cogs." + cog.stem
    logger.debug(f"Loading cog {cog_name}")
    try:
        client.load(cog_name)
    except Exception:
        logger.exception(f"Could not load cog: {cog_name}")

client.start()
