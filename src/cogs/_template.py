import logging

import interactions

from utils.environment import BOT_SCOPE
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class TemplateCog(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client
        logger.info(f"{__class__.__name__} cog registered")

    @interactions.extension_command(
        name="test", description="test command", scope=BOT_SCOPE
    )
    async def test_cmd(self, ctx: interactions.CommandContext):
        await ctx.send("Test")


def setup(client: interactions.Client):
    TemplateCog(client)
