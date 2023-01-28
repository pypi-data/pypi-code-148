r"""
Description
-----------

Options
-------

.. program:: flasket

.. option:: -l HOST, --listen HOST

   The ip to listen on (default: localhost)

.. option:: -p PORT, --port PORT

   The port to listen on (default: 8080)

.. option:: -c CFGFILE, --cfgfile CFGFILE

   Use CFGFILE as configuration file, otherwise first file found in
   search path is used. (default search path: (...))

.. option:: --ui, --no-ui

   Enable the OpenAPI UI. Disable with :option:`--no-ui`. (default: enabled)

.. option::  -w WORKERS, --workers WORKERS

   Number of thread workers. (default: 0. If 0, cpu to use is (cpu_count * 2) with a maximum
   of 8; if negative, cpu to use is (cpu_count * 2) with no maximum.)

.. option::  --pidfile FILE

   A filename to use for the PID file. (default: none)

Usage
-----

.. program:: flasket

.. code-block:: python

  #!/usr/bin/env python3

  from flasket import make_flasket

  if __name__ == "__main__":
      flasket = make_flasket(__file__, "gunicorn", cfgname="example.yml")
      flasket.run()

"""
import argparse
import logging
import multiprocessing
import typing as t

from attrs import define, field
from flask.logging import default_handler
from gunicorn.app.base import BaseApplication
from torxtools.pathtools import expandpath

from ..flasket import Flasket

__all__: t.List[str] = [
    "GunicornApplication",
    "GunicornFlasketCreator",
]


class GunicornFlasketCreator:
    @staticmethod
    def flasket(*args: t.Any, **kwargs: t.Any) -> Flasket:
        app = GunicornApplication(*args, **kwargs)
        return app._flasket

    @staticmethod
    def force_cfg(cfg: t.Dict["str", t.Any]) -> None:
        cfg["debug"] = False

    @staticmethod
    def add_arguments(defaults: t.Dict["str", t.Any], parser: argparse.ArgumentParser) -> None:
        """
        Adds Gunicorn middleware specific command line arguments :option:`--workers`, :option:`--pidfile`
        to the ArgumentParser.

        Parameters
        ----------
        defaults:

            a dictionnary containing default values

        parser: argparse.ArgumentParser

            a parser on which `add_argument` will be called
        """
        workers = defaults["workers"]
        pidfile = defaults["pidfile"]
        if not pidfile:
            pidfile = "none"

        # fmt: off
        parser.add_argument(
            "-w", "--workers", metavar="WORKERS", type=int,
            help=f"Number of thread workers. (default: {workers}. If 0, cpu to use is (cpu_count * 2) with a maximum of 8; if negative, cpu to use is (cpu_count * 2) with 8 maximum.)",
        )
        parser.add_argument(
            "--pidfile", metavar="FILE", type=str,
            help=f"A filename to use for the PID file. (default: {pidfile})",
        )
        # fmt: on


class GunicornApplication(BaseApplication):  # type: ignore[misc]
    # .venv/lib/python3.9/site-packages/gunicorn/app/base.py
    """
    Gunicorn WSGI application class
    """

    @staticmethod
    def _get_cpu_workers(workers: int) -> int:
        """
        Return the number of workers gunicorn should start with.
        Impose a max limit to avoid overloading the host.

        Parameters
        ----------
        workers: int

            number of workers configured

        Returns
        -------
        int
        """
        if workers > 0:
            return workers

        # Do not overload the host with a default value too large
        # if it's a container, it could report host cpus
        cpus = max((multiprocessing.cpu_count() * 2), 1)
        if workers == 0:
            return min(cpus, 8)
        return cpus

    # pylint: disable=abstract-method
    # http://docs.gunicorn.org/en/stable/custom.html
    def __init__(
        self,
        *args: t.Any,
        cfg: t.Dict[str, t.Any],
        rootpath: str = None,
        options: t.Dict[str, t.Any] = None,
        **kwargs: t.Any,
    ) -> None:
        """
        Initialize a Flasket application, and configure Gunicorn

        Parameters
        ----------
        cfg: dict

            dictionary containing configuration for the application

        rootpath: str

            location from where to load packages
        """
        self._flasket = GunicornFlasket(*args, gunicorn=self, cfg=cfg, rootpath=rootpath, options=options, **kwargs)

        # Rework the configuration
        cfg = self._flasket.config["server"]
        cfg["workers"] = self._get_cpu_workers(cfg["workers"])
        self.options = {
            "bind": f"{cfg['listen']}:{cfg['port']}",
            "pidfile": expandpath(cfg.get("pidfile")),
            "workers": cfg["workers"],
            "accesslog": "/dev/null",
            "errorlog": "/dev/null",
        }

        self._flasket.logger.info(f"Starting {cfg['workers']} workers...")
        super().__init__()

        # Use the Flask logger to log identically between flask and gunicorn
        # We have to specify a null FileStream handler, we'll remove it on first call
        # by using the _gunicorn identifier
        logger = logging.getLogger("gunicorn.error")
        default_handler._gunicorn = False
        logger.addHandler(default_handler)

    def init(self, parser: t.Any, opts: t.Any, args: t.Any) -> None:
        """
        Overloaded abstract method.
        """
        raise NotImplementedError

    def load_config(self) -> None:
        """
        Overloaded abstract method.

        Load Gunicorn configuration ourselves.
        """
        # Pass the configuration down to gunicorn.app.base.BaseApplication
        cfg = {k: v for k, v in self.options.items() if k in self.cfg.settings and v is not None}
        for k, v in cfg.items():
            self.cfg.set(k.lower(), v)

    def load(self) -> "Flasket":
        """
        Overloaded abstract method.

        Return a callable __call__ WSGI application
        """
        return self._flasket


@define(kw_only=True, slots=False)
class GunicornFlasket(Flasket):
    """
    Gunicorn specific Flasket
    """

    _gunicorn: GunicornApplication = field()

    def run(self) -> None:
        """
        Override run() since we don't take any parameters
        """
        self._gunicorn.run()
