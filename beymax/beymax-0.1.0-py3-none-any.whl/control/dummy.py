from .base import AbstractControlInterface
import aiofiles
import yaml
import logging
import os
from io import StringIO
import discord
import sys

logger = logging.getLogger('beymax.control.dummy')

class DummyControlInterface(AbstractControlInterface):
	"""
	Simple single-shard control interface with no remote.
	Meant for debugging or simple deployments
	"""

	def __init__(self, token, suites, config_path=None):
		super().__init__()
		self.token = token
		if config_path is None:
			config_path = os.environ.get("BEYMAX_DUMMYCTL_CONFIG_PATH", default="./config.yml")
		self.config_path = config_path
		self._command_suites = suites
		self.primary_guild = None

	@property
	def commandSuites(self):
		return self._command_suites
	
	async def ready(self):
		"""
		This is a no-op for the dummy controller
		"""
		return

	def add_config_command(self, client):
		"""
		This is a no-op for the dummy controller.
		There is no /config command
		"""
		return
	
	async def check_start_shard(self, ready_token):
		"""
		Return the static shard-id and bot token
		"""
		return 0, self.token, {}

	async def heartbeat(self):
		"""
		Currently a no-op but will probably take care of some internal
		maintenance actions in the future
		"""
		return
	
	async def pre_start(self):
		"""
		Startup tasks
		"""
		# Dummy controller will always need schema. Subscribe to after:schema and create db metadata
		@self.client.subscribe('after:schema', once=True)
		async def create_db_schema(client, event, db):
			await db.connection.run_sync(db.base.metadata.create_all)
			await db.connection.commit()

		@self.client.subscribe('before:ready', once=True)
		async def enforce_primary_server(client, event):
			primary_guild_id = await self.config_get('primary_guild')
			if primary_guild_id is not None:
				self.primary_guild = discord.utils.get(
					self.client.guilds,
					id=primary_guild_id
				)
				if self.primary_guild is None:
					logger.critical("Primary guild set but no matching guild was found")
					sys.exit("Primary guild set, but no matching guild was found")
				else:
					logger.info("Validated primary guild: {}".format(self.primary_guild.name))
			else:
				logger.warning("No primary guild set in configuration. This is not supported behavior")
			if self.primary_guild is not None:
				await self.leave_nonprimary_guilds(*self.client.guilds)
			for guild in self.client.guilds:
				logger.debug("Connected to guild {} ({})".format(guild.name, guild.id))

	async def config_get(self, *keys, default=None):
		async with aiofiles.open(self.config_path, 'r') as r:
			config = yaml.load(StringIO(await r.read()), Loader=yaml.SafeLoader)
		for key in keys:
			try:
				config = config[key]
			except KeyError:
				logger.debug("Requested config key {} not found".format('.'.join(keys)))
				return default
		return config
	
	async def leave_nonprimary_guilds(self, *guilds):
		if self.primary_guild is not None:
			for guild in guilds:
				if guild.id != self.primary_guild.id:
					try:
						logger.info("Leaving secondary guild {}".format(guild.name))
						await (discord.utils.get(
								guild.channels,
								name='general',
								type=discord.ChannelType.text
							)).send_message(
							"Unfortunately, this instance of {0} is not configured"
							" to run on multiple servers. Please contact the owner"
							" of this instance, or run your own instance of {0}."
							" Goodbye!".format(self.user.name)
						)
					except:
						pass
					await guild.leave()

	async def on_guild_join(self, guild):
		"""
		Coroutine. Handler for joining guilds. Do not override.
		If you wish to add handling for joining guilds use @bot.subscribe('guild_join')

		If a primary guild is defined and this is not the primary guild, leave it.
		Otherwise, print a warning that a primary guild is not defined
		"""
		if self.primary_guild is not None and self.primary_guild.id != guild.id:
			await self.leave_nonprimary_guilds(guild)
	
	def suite_enabled_in_guild(self, suite, guild):
		"""
		Dummy controller does not support suite/command toggles
		"""
		return True
	
	def command_enabled_in_guild(self, suite, guild):
		"""
		Dummy controller does not support suite/command toggles
		"""
		return True


	