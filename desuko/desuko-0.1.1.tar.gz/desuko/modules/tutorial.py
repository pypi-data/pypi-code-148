"""'Hello, World' module for Desuko."""
import discord

from desuko.loader import Loader

__NAME__ = 'tutorial'
__DESC__ = '"Hello, World" module for Desuko'


class Module:
    """Example module class."""

    def __init__(self, loader: Loader, slash_group: discord.SlashCommandGroup, _: dict):
        """Initialize this module.

        Args:
            loader (Loader): Loader to communicate with
            slash_group (discord.SlashCommandGroup): Discord slash command group
            _ (dict): Configuration for this module
        """
        self.slash_group = slash_group
        loader.subscribe('desuko.bot.register_slash', self.register_slash)

    def register_slash(self) -> None:
        """Register slash commands."""
        self.slash_group.command()(self.desuko)

    async def desuko(self, ctx):
        """'Hello, Desuko!' command.

        Args:
            ctx (ApplicationContext): Application context
        """
        await ctx.respond('Hello, Desuko!')
