import asyncio
import importlib
import logging
import os
import signal
import sys

from .app import AipoApp

logger = logging.getLogger("aipo")


class Worker:
    """Aipo worker class.
    This class is responsible for starting and stopping the Aipo server.
    """

    start_future: asyncio.Future
    stop_future: asyncio.Future

    def __init__(self, app: str, loop_name: str | None = None) -> None:
        self._setup_loop(loop_name)
        self.loop = asyncio.get_event_loop()

        self._setup_signal_handlers()
        self.app = self._get_app(app)
        self._configure_logging()

    def exec_from_cmd(self) -> None:
        exit_code = os.EX_OK

        try:
            self.start_future = asyncio.ensure_future(
                self.app.start_server(), loop=self.loop
            )
            self.loop.run_until_complete(self.start_future)
            self.loop.run_until_complete(self.stop_future)
        except Exception as e:
            logger.critical("Critical exception stopped Aipo server")
            logger.exception(e)
            exit_code = os.EX_SOFTWARE
        finally:
            self._shutdown_loop()

        sys.exit(exit_code)

    def _shutdown_loop(self) -> None:
        while self.loop.is_running():
            self.loop.stop()
            self.loop.run_until_complete(asyncio.sleep(0.5))
        self.loop.close()

    def _get_app(self, app: str) -> AipoApp:
        module_name, app_name = app.split(":")
        module = importlib.import_module(module_name)
        return getattr(module, app_name)

    def _setup_loop(self, loop_name: str | None = None) -> None:
        if loop_name is None:
            return

        if asyncio._get_running_loop() is not None:
            raise RuntimeError("Event is already running.")

        if loop_name == "uvloop":
            import uvloop

            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        elif loop_name == "asyncio":
            pass
        else:
            raise ValueError(f"Unknown loop name: {loop_name}")

    def _setup_signal_handlers(self) -> None:
        self.loop.add_signal_handler(signal.SIGINT, self._signal_handler)
        self.loop.add_signal_handler(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self) -> None:
        if not self.stop_future:
            self.stop_future = asyncio.ensure_future(
                self.app.stop_server(), loop=self.loop
            )

    def _configure_logging(self) -> None:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
