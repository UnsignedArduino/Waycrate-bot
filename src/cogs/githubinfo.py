import logging

import interactions

from filesystem import Interface
from utils.environment import BOT_SCOPE
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class GitHubInfoCog(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client
        logger.info(f"{__class__.__name__} cog registered")

    @interactions.extension_command(
        name="cat", description="Read from a file!", scope=BOT_SCOPE,
        options=[
            interactions.Option(
                name="path",
                description="The file to read from.",
                type=interactions.OptionType.STRING,
                required=True
            )
        ]
    )
    async def cat(self, ctx: interactions.CommandContext, path: str):
        await ctx.send(f"```\n{Interface.cat(path)}\n```")

    @interactions.extension_command(
        name="ls", description="List the files in a directory!",
        scope=BOT_SCOPE,
        options=[
            interactions.Option(
                name="path",
                description="The directory to list in.",
                type=interactions.OptionType.STRING,
                required=False
            )
        ]
    )
    async def ls(self, ctx: interactions.CommandContext, path: str = "/"):
        await ctx.send(f"```\n{Interface.ls(path)}\n```")

    @interactions.extension_command(
        name="tree",
        description="Print a hierarchy of files and directories!",
        scope=BOT_SCOPE,
        options=[
            interactions.Option(
                name="path",
                description="The directory to list in.",
                type=interactions.OptionType.STRING,
                required=False
            )
        ]
    )
    async def tree(self, ctx: interactions.CommandContext, path: str = "/"):
        lines = Interface.tree(path).split("\n")
        groups = [""]
        MAX_CHARS = 2000 - 8
        for line in lines:
            if len(groups[-1]) + len(line) + 2 > MAX_CHARS:
                groups.append(line + "\n")
            else:
                groups[-1] += line + "\n"
        for group in groups:
            await ctx.send(f"```\n{group}\n```")


def setup(client: interactions.Client):
    GitHubInfoCog(client)
