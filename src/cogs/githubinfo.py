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
        await self.send_result(ctx, Interface.cat(path))

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
        await self.send_result(ctx, Interface.ls(path))

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
        await self.send_result(ctx, Interface.tree(path))

    async def send_result(self, ctx: interactions.CommandContext,
                          result: dict):
        # https://stackoverflow.com/a/64933270/10291933
        # Additionally, the characters in all title, description, field.name,
        # field.value, footer.text, and author.name fields must not exceed
        # 6000 characters in total. Violating any of these constraints will
        # result in a Bad Request response.
        # +-------------+------------------------+
        # |    Field    |         Limit          |
        # +-------------+------------------------+
        # | title       | 256 characters         |
        # | description | 4096 characters*       |
        # | fields      | Up to 25 field objects |
        # | field.name  | 256 characters         |
        # | field.value | 1024 characters        |
        # | footer.text | 2048 characters        |
        # | author.name | 256 characters         |
        # +-------------+------------------------+
        if len(result['output']) < 1024 - 8:
            embeds = interactions.Embed(color=0 if result["success"]
                                             else 0xFF0000)
            embeds.add_field(name=f"`{result['command']}`",
                             value=f"```\n{result['output']}\n```")
        else:
            lines = result["output"].split("\n")
            groups = [""]
            MAX_CHARS = 1024 - 8
            for line in lines:
                if len(groups[-1]) + len(line) + 2 > MAX_CHARS:
                    groups.append(line + "\n")
                else:
                    groups[-1] += line + "\n"
            groups = tuple(f"```\n{group}\n```" for group in groups)
            embeds = []
            for index, text in enumerate(groups):
                embed = interactions.Embed(color=0 if result["success"]
                                                 else 0xFF0000)
                embed.add_field(name=f"`{result['command']}` "
                                     f"({index}/{len(groups) - 1})",
                                value=text)
                embeds.append(embed)
        await ctx.send(embeds=embeds)


def setup(client: interactions.Client):
    GitHubInfoCog(client)
