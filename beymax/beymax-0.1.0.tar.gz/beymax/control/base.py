import abc
import asyncio
import logging
from ..client import Client
import signal
import sys

logger = logging.getLogger("beymax.control.base")

class AbstractControlInterface(abc.ABC):
	"""
	This class lays out the API that Controllers are expected to provide to bot shards.
	Every client must be connected to a Control Interface, and defers to the interface
	for any decisions beyond the scope of a single shard
	"""

	def __init__(self):
		self.client = None
	
	async def __aenter__(self):
		"""
		ControlInterface should be used as a context manager
		"""
		return self

	async def __aexit__(self, exc_inf, tb, stack):
		"""
		Context exit is a no-op on the base class
		"""
		pass

	@abc.abstractproperty
	def commandSuites(self):
		"""
		Returns a list of CommandSuite instances that the control interface intends to enable
		These suites will be enabled on created clients.
		It does not mean that these suites have been ACTIVATED in any particular guild
		"""
		pass

	@abc.abstractmethod
	async def ready(self):
		"""
		This coroutine should take any local actions needed to prepare,
		and then report itself as ready to the remote. If this method returns
		anything (such as a token or other information received from the remote)
		it is passed to .check_start_shard()
		Relevent logging configuration should take place here
		"""
		pass

	async def start(self, start_wait_interval_s=10):
		"""
		This coroutine is responsible for calling .ready(),
		then waiting until .check_start_shard() returns a shard ID and token
		Anything returned by .ready() is passed to .check_start_shard().
		Finally, it calls .create_client() and client.start()
		This coroutine does not return until the shard has been stopped
		"""
		ready_token = await self.ready()
		logger.info("Control Interface has checked in and is ready. Waiting for shard start")
		shard_id, bot_token, metadata = await self.check_start_shard(ready_token)
		while bot_token is None:
			await asyncio.sleep(start_wait_interval_s)
			shard_id, bot_token, metadata = await self.check_start_shard(ready_token)
		logger.info("Starting shard ID {}".format(shard_id))
		async with self.create_client(shard_id=shard_id, control_meta=metadata) as client:
			await client.async_init()
			client.attachSuites(*self.commandSuites)
			self.add_config_command(client)
			logger.debug("Client starting now")
			await self.pre_start()
			await client.start(bot_token)

	def start_loop_interrupt_safe(self):
		"""
		Control logic for graceful event loop creation and shutdown.
		Installs signal handlers for SIGTERM, SIGINT, and SIGHUP for a quick, graceful shutdown.
		Designed to work well on the command line (where ctrl+c sends SIGINT) and in docker containers (where docker stop sends SIGTERM)
		"""
		loop = asyncio.get_event_loop()

		shutdown_complete = asyncio.Event()
		
		async def enter_and_start():
			async with self:
				await self.start()

		for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
			loop.add_signal_handler(
				sig,
				(lambda sig=sig:loop.create_task(self.client.shutdown(signal=sig, event=shutdown_complete)) if self.client is not None else sys.exit(1))
			)

		try:
			loop.create_task(enter_and_start())
			loop.run_until_complete(loop.create_task(shutdown_complete.wait()))
		finally:
			logger.info("Controller finished. Shutdown complete")
			loop.close()
			

	
	async def pre_start(self):
		"""
		Lifecycle hook for any activity that should take place after the client
		has been created, and before the client is started
		"""
		pass
		
	@abc.abstractmethod
	def add_config_command(self, client):
		"""
		This method is responsible for defining the GLOBAL /config command
		for a shard
		"""
		pass

	def create_client(self, shard_id, control_meta):
		"""
		This is responsible for instantiating a client.
		"""
		self.client = Client(control_interface=self, shard_id=shard_id, control_meta=control_meta)
		return self.client
	
	@abc.abstractmethod
	async def check_start_shard(self, ready_token):
		"""
		This method is responsible for checking if the remote is ready for the shard to start.
		ready_token is whatever the return value from self.ready() was, and can be used in any way.
		This method must return (Any), None, (Any) to indicate that the remote IS NOT ready for the shard
		This method must return (int), (str), (dict) to indicate that the remote IS ready for the shard
		"""
		pass

	@abc.abstractmethod
	async def heartbeat(self):
		"""
		This method is responsible for pinging the remote and checking for status updates.
		This will be subscribed to the 'heartbeat' event which is sent every 30 seconds
		This method should take care of any actions needed, as the return value is ignored by the client
		"""
		pass

	@abc.abstractmethod
	async def config_get(self, *keys, default=None):
		"""
		This method is responsible for retrieving a value from config
		"""
		pass

	@abc.abstractmethod
	async def on_guild_join(self, guild):
		"""
		This method allows the controller to respond to guild_join events.
		The controller may take any actions here (such as leaving the guild to enforce primary_server mode)
		"""
		pass

	@abc.abstractmethod
	def suite_enabled_in_guild(self, suite, guild):
		"""
		This should a boolean indicating if the suite is currently enabled in the guild
		This *MUST* return True for suites where CommandSuite.forced == True
		"""
		pass

	@abc.abstractmethod
	def command_enabled_in_guild(self, suite, guild):
		"""
		This should a boolean indicating if the command (or context) is currently enabled in the guild
		"""
		pass

	# skeleton for WIP callback/wait-for system
	def wait_for_event(self, event_name):
		# Create a future
		# Add an entry in a dictionary event_name -> future
		# Return the future for the client to wait on
		# In heartbeat(), when the remote is satisfied the event is complete, mark the future as complete
		# This is a template for future use with the file upload command and waiting for callbacks
		raise NotImplementedError("This function is still a work in progress")


"""
Pre planning:
* ControlInterface should be instantiated with minimum config to connect to central controller (if any). DummyControlInterface has not central controller
* ControlInterface should first authenticate with the remote (if necessary)
* ControlInterface should perform any ready-checks then report itself as ready to the remote
* ControlInterface should wait until the remote confirms to start the shard. Remote is also responsible for providing token and shard id
* ControlInterface should then instantiate and start a client instance
* All configuration, including database connection information, is read from the controller
* The bot should be able to connect to the database once it has relevant connection details without using the controller each time.
* The ControlInterface is responsible for adding the global /config command to a client
* The schema and migration events will remain in the client, however, the client will no longer call await self.db.connection.run_sync(self.db.base.metadata.create_all)
  * The controller is now responsible for creating database schema. The remote may request that a shard create the schema or not.
"""