import logging

import interactions

from utils.environment import BOT_SCOPE
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class GitHubInfoCog(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client
        logger.info(f"{__class__.__name__} cog registered")

    @interactions.extension_command(
        name="cat", description="Read from a file!", scope=BOT_SCOPE
    )
    async def cat(self, ctx: interactions.CommandContext):
        await ctx.send("cat")

    @interactions.extension_command(
        name="ls", description="List the files in a directory!",
        scope=BOT_SCOPE
    )
    async def ls(self, ctx: interactions.CommandContext):
        await ctx.send("ls")

    @interactions.extension_command(
        name="tree",
        description="Print a hierarchy of files and directories!",
        scope=BOT_SCOPE
    )
    async def tree(self, ctx: interactions.CommandContext):
        await ctx.send("tree")


def setup(client: interactions.Client):
    GitHubInfoCog(client)
