import asyncio
import inspect
import logging
import sys

from logging import Logger, Handler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from dataclasses import replace
from typing import Any, Awaitable, Callable

from aiorun import run
from asyncio.exceptions import CancelledError
from case_insensitive_dict import CaseInsensitiveDict
from dotenv import load_dotenv, find_dotenv

from door.decorators import PluginMetadata
from door.dispatch import EventDispatcher
from door.plugins import DoorBasePlugin, PluginHandler
from door.sentry import configure_sentry
from door.settings import import_settings
from door.slack import Slack
from door.utils import find_shortest_indent
from door.utils.plugins import import_plugins

from sentry_sdk import start_transaction, start_span

__all__ = ["Door", "start"]


def start(
    loop: asyncio.AbstractEventLoop,
    log_level: int = logging.INFO,
    settings: CaseInsensitiveDict | None = None,
    *,
    stdout: bool = False,
) -> None:
    if settings:
        found_local_settings = True
    else:
        # populate environment with settings from a .env file (like DOOR_SLACK_API_TOKEN)
        load_dotenv(find_dotenv())
        # get settings from "local/settings.py" module
        settings, found_local_settings = import_settings()

    formatter = logging.Formatter(fmt="{asctime} [{levelname:.1s}] {name} ({filename}:{funcName}:{lineno})  {message}", style="{")
    logging.Formatter.default_msec_format = "%s.%03d"

    # log errors and above to stderr (unless `-o` arg was given, then use stdout)
    stdio_handler = logging.StreamHandler(sys.stdout if stdout else sys.stderr)
    stdio_handler.setLevel(log_level if stdout else logging.ERROR)
    stdio_handler.setFormatter(formatter)
    logging_handlers: list[Handler] = [stdio_handler]

    # if "LOG_FILE" is defined in settings, create daily logs at the specified level
    if settings and "LOG_FILE" in settings and Path(settings["LOG_FILE"]).parent.exists():
        logfile_handler = TimedRotatingFileHandler(settings["LOG_FILE"], when="midnight")
        logfile_handler.setLevel(log_level)
        logfile_handler.setFormatter(formatter)
        logging_handlers.append(logfile_handler)

    # configure loggers and root log level
    logging.basicConfig(handlers=logging_handlers, level=log_level)

    logger = logging.getLogger(__name__)

    if not found_local_settings:
        logger.warning("No 'local_settings' found")

    if settings:
        bot = Door(settings=settings, loop=loop, logger=logger)
        run(bot.run(loop), loop=loop, shutdown_callback=bot.stop(), stop_on_unhandled_errors=True)


class Door:
    _slack: Slack
    _dispatcher: EventDispatcher
    _loop: asyncio.AbstractEventLoop
    _settings: CaseInsensitiveDict
    _help = {}
    # a dict of all the events with handlers, plus "message" and "link_shared" events
    _plugin_events: dict[str, list[PluginHandler]] = {
        "message": [],
        "link_shared": [],
    }

    def __init__(
        self, settings: CaseInsensitiveDict, loop: asyncio.AbstractEventLoop | None = None, logger: Logger | None = None
    ) -> None:
        self._settings = settings
        self._loop = loop or asyncio.get_event_loop()
        self.logger = logger or logging.getLogger(__name__)

        if project_id := configure_sentry(self._settings):
            self.logger.info(f"Sending errors and events to Sentry (project #{project_id})")

        if "SLACK_BOT_TOKEN" not in self._settings:
            self.logger.error("Missing SLACK_BOT_TOKEN")
            sys.exit(1)

        if "SLACK_APP_TOKEN" not in self._settings:
            self.logger.error("Missing SLACK_APP_TOKEN")
            sys.exit(1)

        # the Slack class must be instantiated before loading any plugins since they depend on stuff it configures
        self._slack = Slack(settings=self._settings, logger=self.logger, loop=self._loop)

        self.logger.info("Loading plugins")
        with start_transaction(op="startup", name="load plugins"):
            self.load_plugins()
        for event, handlers in self._plugin_events.items():
            for handler in handlers:
                self.logger.debug(f"Registered '{event}' handler: {handler.class_name}:{handler.fn_name}()")

        self._dispatcher = EventDispatcher(self._plugin_events, self._settings)

    def load_plugins(self) -> None:
        for plugin in self._settings["PLUGINS"]:
            for class_name, cls in import_plugins(plugin):
                if issubclass(cls, DoorBasePlugin) and cls is not DoorBasePlugin:
                    self.logger.debug(f"Found a Door plugin: {plugin}")
                    try:
                        instance = cls()
                    except ValueError as e:
                        self.logger.error(f"{class_name} plugin disabled during __init__: {e}")
                        continue

                    # Initialize the plugin
                    with start_span(op="startup", description=f"init {class_name}") as span:
                        try:
                            if inspect.iscoroutinefunction(instance.init):
                                # still in __init__ so can't await yet (type checking doesn't like it not being defined as async)
                                self._loop.run_until_complete(instance.init(self._slack.app))
                            else:
                                instance.init(self._slack.app)
                        except ValueError as e:
                            self.logger.error(f"{class_name} plugin disabled during init(): {e}")
                            span.set_status("internal_error")
                            continue
                        else:
                            span.set_status("ok")

                    self._register_plugin(class_name, instance)
                    self.logger.info(f"Loaded plugin: {class_name}")

        # TODO: initialize other stuff here (storage handlers?)

    async def run(self, loop: asyncio.AbstractEventLoop) -> None:
        try:
            self._dispatcher.start()
        except Exception as e:
            # If we get any errors during startup, don't even try to continue
            loop.stop()
            self.logger.exception(f"Error during startup: {e}")

        try:
            # TODO: start the scheduler
            # Scheduler(settings=self._settings, loop=self._loop).start()

            # TODO: start http server (for future API... allow plugins to register endpoints?)
            # runner = await self._start_http_server()

            self.logger.info("Opening Door...")
            await self._slack.init_async_handler(self._settings)
            await self._slack.handler.connect_async()
            await asyncio.sleep(float("inf"))
        except CancelledError:
            pass

    async def stop(self) -> None:
        self.logger.info("Closing Door...")
        await self._slack.handler.close_async()

    def _register_plugin(self, plugin_class: str, cls_instance: DoorBasePlugin) -> None:
        methods = inspect.getmembers(cls_instance, predicate=inspect.ismethod)

        if cls_instance.__doc__:
            class_help = cls_instance.__doc__.splitlines()[0]
        else:
            class_help = plugin_class
        self._help[class_help] = self._help.get(class_help, {})

        for name, fn in methods:
            # check if the method is Door-decorated
            if hasattr(fn, "metadata"):
                assert isinstance(fn.metadata, PluginMetadata)
                self._register_plugin_listeners(plugin_class, fn.metadata, cls_instance, name, fn, class_help)

    def _register_plugin_listeners(
        self,
        plugin_class: str,
        metadata: PluginMetadata,
        cls_instance: DoorBasePlugin,
        fn_name: str,
        fn: Callable[..., Awaitable[Any]],
        class_help: str,
    ) -> None:
        fq_fn_name = f"{plugin_class}.{fn_name}"

        if fn.__doc__:
            self._help[class_help][fq_fn_name] = self._parse_help(fn.__doc__)

        handler = PluginHandler(class_inst=cls_instance, class_name=plugin_class, fn_name=fn_name, function=fn)

        if events := metadata.events:
            for event_type in events:
                event_handler = self._plugin_events.get(event_type, [])
                if event_type in ("message", "link_shared"):
                    raise ValueError(f"Use the @{event_type} decorator to process '{event_type}' events")
                if not event_handler or event_type in (
                    "message_changed",
                    "message_deleted",
                    "member_joined_channel",
                    "message_callback",
                    "file_share",
                ):
                    # allow multiple handlers for "message_changed"/"message_deleted"/"file_share" message subtype
                    # events, along with "member_joined_channel" and our synthetic "message_callback" event
                    event_handler.append(handler)
                    self._plugin_events[event_type] = event_handler
                else:
                    # Bolt is architected around a "one acknowledgement per event" (and why
                    # we have to handle some events "specially" in the dispatcher)
                    raise ValueError(f"'{event_type}' is already registered: {event_handler}")

        if msg_regexps := metadata.message_regexps:
            message_handlers = self._plugin_events.get("message", [])
            for regex in msg_regexps:
                message_handlers.append(replace(handler, regex=regex))

        if url_regexps := metadata.link_shared_regexps:
            link_shared_handlers = self._plugin_events.get("link_shared", [])
            for url_regex in url_regexps:
                link_shared_handlers.append(replace(handler, url_regex=url_regex))

        # TODO: handle future "schedule"-type decorator
        # e.g. Scheduler.get_instance().add_job(...)

    @staticmethod
    def _parse_help(doc: str) -> dict[str, str | list[str] | None]:
        doclines: list[str] = doc.splitlines()
        summary_items: list[str] = doclines[0].split(":")

        if len(doclines) > 1:
            details = doclines[1:]
            try:
                # Trim off leading/trailing lines if they are empty
                if details[0].strip() == "":
                    details = details[1:]
                if details[-1].strip() == "":
                    details = details[:-1]

                desc_min_indent = find_shortest_indent(details)
                details = [line[desc_min_indent:] for line in details]
            except IndexError:
                pass
        else:
            details = None

        if len(summary_items) > 1:
            command = summary_items[0].strip()
            summary = summary_items[1].strip()
        else:
            command = "??"
            summary = summary_items[0].strip()

        return {"command": command, "summary": summary, "details": details}
