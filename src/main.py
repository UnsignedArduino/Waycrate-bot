import logging
from pathlib import Path

import interactions

from utils.environment import BOT_TOKEN
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

COGS_PATH = Path.cwd() / "cogs"

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
    module.stem for module in COGS_PATH.rglob("*")
    if module.name not in ("__init__.py",) and
       module.suffix == ".py" and
       not module.name.startswith("_")
]

logger.info(f"Importing {len(cogs)} cog{'s' if len(cogs) != 1 else ''}")

for cog in cogs:
    cog_name = "cogs." + cog
    logger.debug(f"Loading cog {cog_name}")
    try:
        client.load(cog_name)
    except Exception:
        logger.exception(f"Could not load cog: {cog_name}")

client.start()
