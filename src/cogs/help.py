import logging

import interactions

from utils.environment import BOT_SCOPE
from utils.embed import send_result
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class HelpCog(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client
        logger.info(f"{__class__.__name__} cog registered")

    @interactions.extension_command(
        name="help", description="Prints shell commands defined internally.",
        scope=BOT_SCOPE
    )
    async def help(self, ctx: interactions.CommandContext):
        await send_result(ctx, {
            "command": "help",
            "output": "HELPPPPPPPPPPP",
            "success": True
        })


def setup(client: interactions.Client):
    HelpCog(client)
