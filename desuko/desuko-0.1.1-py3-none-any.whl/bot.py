"""desuko.bot - Discord bot for Desuko."""
import logging

import discord

from desuko.loader import Loader

logger = logging.getLogger(__name__)


class DesukoBot:
    """Discord bot class."""

    def __init__(self, config: dict, modules: dict):
        """Initialize a bot.

        Args:
            config (dict): Desuko configuration
            modules (dict): Loaded modules
        """
        self.config = config
        self.bot = discord.Bot(
            auto_sync_commands=False,
            debug_guilds=self.config.get('debug_guilds'),
        )
        self.loader = Loader(self.bot.create_group, modules)

        self.register_slash = self.loader.handler(self._register_slash)
        self.prepare_bot = self.loader.handler(self._prepare_bot)
        self.on_ready = self.loader.handler(self._on_ready, return_async=True)
        self.shutdown = self.loader.handler(self._shutdown)

        self.loader.init_modules()
        self.bot.listen('on_ready')(self.on_ready)

    def _register_slash(self) -> None:
        """Register slash commands."""
        self.bot.slash_command(description='Say hello!')(self.hello)

    def _prepare_bot(self) -> None:
        """Prepare bot before running.

        This function exists only to handle its subscribers. By using it, we ensure,
        that Desuko is completely loaded (in terms of modules).
        """

    def _shutdown(self) -> None:
        """Gracefully shutdown the bot.

        This function exists only to handle its subscribers. By using it, we ensure,
        that Desuko is closed correctly.
        """
        logger.warning('Graceful shutdown initiated. Please wait...')

    async def _on_ready(self):
        """Desuko is connected to Discord successfully."""
        await self.bot.sync_commands()
        logger.warning('Ready to go! We have logged in as %s.', self.bot.user)

    async def hello(self, ctx):
        """Hello command.

        Args:
            ctx (ApplicationContext): Application context
        """
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name='Desuko', value='Hello', inline=True)
        await ctx.send_response(embed=embed)

    def run(self) -> None:
        """Run the Discord bot."""
        self.register_slash()
        self.prepare_bot()
        self.bot.run(self.config['token'])
        # TODO: Implement shutdown initiated by modules
