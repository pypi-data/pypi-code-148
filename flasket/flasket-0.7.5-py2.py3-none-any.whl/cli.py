# pylint: disable=anomalous-backslash-in-string
r"""
Description
-----------

A FlasketCLI helper is built by composing a :class:`flasket.cli.FlasketCmdline` and
a :class:`flasket.cli.FlasketSettings` class.

The :class:`flasket.middleware.flask.FlasketCLI` and :class:`flasket.middleware.gunicorn.FlasketCLI`
are already preconfigured to use the appropriate FlasketCmdline and FlasketSettings classes.

A binary helper for each is proposed as :program:`flasket-dev` and :program:`flasket`. It can serve
content from this repository.

Classes
-------

.. program:: flasket

FlasketCmdline
^^^^^^^^^^^^^^

.. autoclass:: FlasketCmdline
  :show-inheritance:
  :members: __call__, add_arguments, transform

FlasketSettings
^^^^^^^^^^^^^^^

.. autoclass:: FlasketSettings
  :show-inheritance:
  :members: __call__

ABCFlasketCli
^^^^^^^^^^^^^

.. autoclass:: ABCFlasketCli
  :show-inheritance:
  :members: run, _run

Example\s
---------

Refer to the :ref:`Quickstart` section for usage example.

"""
import abc
import argparse
import os
import sys
import typing as t

from attr import define, field
from boltons.iterutils import remap
from torxtools import xdgtools
from torxtools.cfgtools import which
from torxtools.ctxtools import suppress_traceback
from torxtools.pathtools import expandpath
from yaml import safe_load

from ._utils import deepmerge
from .defaults import default_configuration

__all__ = ["FlasketCmdline", "FlasketSettings", "ABCFlasketCli"]

# Used to determine that type is not a lambda
dummy = lambda: 1  # pylint: disable=unnecessary-lambda-assignment


def _read(cfgfile: str) -> t.Dict:
    """
    Convenience function in order to be mocked.

    Parameters
    ----------
    cfgfile: str

        a single path representing a yaml file.

    Returns
    -------
    dict:

        a dictionary
    """
    with open(cfgfile, encoding="UTF-8") as fd:
        data = safe_load(fd)
    return data or {}


@define(kw_only=True, slots=False)
class _DefaultCfgMixin:
    """
    Parameters
    ----------
    default_cfg: dict, default: :meth:`flasket.defaults.default_configuration`

        Dictionary containing the defaults for configuration file.
        Passed value will be merged with the default factory configuration.
    """

    _default_cfg: t.Dict = field(default=None)

    def __attrs_post_init__(self) -> None:
        """
        Create a merged dict to ensure that unspecified options have our defaults
        """
        ours = default_configuration(self._default_cfg)
        self._default_cfg = deepmerge(ours, self._default_cfg or {})


class FlasketCmdline(_DefaultCfgMixin):
    """
    Base class that defines and parses the command line arguments for FlasketCLI.

    Parameters
    ----------
    default_cfg: dict, default: :meth:`flasket.defaults.default_configuration`

        Dictionary containing the defaults for the command line arguments.
        Passed value will be merged with the default factory configuration.

    Examples
    --------

        class LocalCmdline(FlasketCmdline):
            def add_arguments(self, parser):
                super().add_arguments(parser)
                parser.add_argument("--foobar", help="How to foobar!")
                return parser


        def main():
            FlasketCLI(cmdline_cfg=LocalCmdline).run()
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        """
        Add middleware specific arguments.

        Parameters
        ----------
        parser: argparse.ArgumentParser

            a parser on which `add_argument` will be called

        Returns
        -------
        argparse.ArgumentParser
        """
        return parser

    def transform(self, args: t.Dict) -> t.Dict:
        """
        Function to convert flat argument list to a dictionary for Flasket configuration.

        Parameters
        ----------
        args: dict

            a flat dictionary, usually the result of argparse.ArgumentParser.parse_args

        Returns
        -------
        dict:

            a valid minimal Flasket configuration dictionary
        """
        # None arguments will be ignored
        # cf. flasket/defaults.py
        # pylint: disable=unnecessary-lambda-assignment
        drop_none = lambda _p, k, v: k is not None and v is not None

        return remap(
            {
                "cfgfile": args.get("cfgfile"),
                "server": {
                    "debug": args.get("debug"),
                    "listen": args.get("listen"),
                    "port": args.get("port"),
                    "ui": args.get("ui"),
                    "workers": args.get("workers"),
                    "pidfile": args.get("pidfile"),
                },
            },
            visit=drop_none,
        )

    def __call__(self, argv: t.List[str] = None) -> t.Dict:
        """
        Parse the argument list argv and return a dictionary augmented with the values
        specified on command line.

        Parameters
        ----------
        argv: list[str], default: None

            Uses :code:`sys.argv[1:]` if None

        Returns
        -------
        dict:

            a Flasket configuration dictionary
        """
        defaults = self._default_cfg

        if argv is None:
            argv = sys.argv[1:]

        # Sets environment variables for XDG paths
        xdgtools.setenv()

        # argument_default=None does not set the default to None for boolean options,
        # so we'll specifically set default=None for those values
        #
        # Default values aren't actually added/set here, but in the FlasketSettings,
        # We only care about values that were specified.
        parser = argparse.ArgumentParser(
            description=defaults["description"],
            argument_default=None,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # Prepare some variables
        cfgname = defaults["cfgname"]
        search_paths = defaults["cfgfile_search_paths"]
        search_paths = [e.format(cfgname=cfgname) for e in search_paths]
        b_ui = {True: "enabled", False: "disabled"}[defaults["server"]["ui"]]

        # fmt: off
        parser.add_argument(
            "-l", "--listen", metavar="HOST",
            help=f'The ip to listen on (default: {defaults["server"]["listen"]})',
        )
        parser.add_argument(
            "-p", "--port", metavar="PORT", type=int,
            help=f'The port to listen on (default: {defaults["server"]["port"]})',
        )
        parser.add_argument(
            "-c", "--cfgfile", metavar="CFGFILE",
            help=f"Use CFGFILE as configuration file, otherwise first file found in search path is used. (default search path: {search_paths})",
        )
        parser.add_argument(
            "--ui", action="store_true", default=None,
            help=f"Enable the OpenAPI UI. Disable with --no-ui. (default: {b_ui})",
        )
        parser.add_argument(
            "--no-ui", action="store_false", default=None, dest="ui",
            help=argparse.SUPPRESS,
        )
        # fmt: on

        # Potentially add extra arguments depending on the middleware
        parser = self.add_arguments(parser)

        # Parse the arguments, transform into a minimal dictionary, and update defaults
        # from ctor
        args = vars(parser.parse_args(argv))
        args = self.transform(args)

        return args


@define(kw_only=True, slots=False)
class FlasketSettings(_DefaultCfgMixin):
    """
    Class that takes the default configuration and merges it with the command line
    configuration and configuration values of the optional configuration file.

    Parameters
    ----------
    default_cfg: dict, default: :meth:`flasket.defaults.default_configuration`

        Dictionary containing the defaults for the command line arguments.
        Passed value will be merged with the default configuration.

    cmdline_cfg: any, default: :class:`flasket.middleware.flask.FlasketCmdline`

        Dictionary, or Callable that returns a dictionary for the command line arguments.
        Defaults to :class:`flasket.middleware.flask.FlasketCmdline`

    forced_cfg: dict, default: None

        Dictionary of settings to force after configuration generation.
    """

    _cmdline_cfg: any = field(default=None)
    _forced_cfg: t.Dict = field(default=None)

    def __attrs_post_init__(self: object) -> None:
        self._forced_cfg = self._forced_cfg or {}
        super().__attrs_post_init__()

    def __call__(self: object, argv: t.List[str] = None) -> t.Dict:
        """
        Parse command line arguments if possible, then parse configuration file,
        and return a configuration dictionary.

        If `cmdline_cfg` is callable, then call it with `default_cfg`. `cmdline_cfg` will
        parse the command line arguments and return a partial configuration dictionary.

        Otherwise, `cmdline_cfg` will be used as-is.

        The configuration file specified by the `cfgfile` key (:option:`--cfgfile`) will
        be selected as the configuration file unless the key is absent.

        If no `cfgfile` key is present, then search for a file named by value of key `cfgname`, and
        located somewhere in the `cfgfile_search_paths` key values.

        The configuration file, if found, will be read.

        Configuration dictionary will then be built by merging command line arguments,
        configuration file, and defaults.

        Parameters
        ----------
        argv: list[str], default: None

            Uses :code:`sys.argv[1:]` if None

        Returns
        -------
        dict:

            a valid Flasket configuration dictionary
        """
        # Get the command line parameters as configuration dictionary
        # pylint: disable=not-callable
        if self._cmdline_cfg is None:
            cmdline_cfg = {}
        elif isinstance(self._cmdline_cfg, dict):
            cmdline_cfg = self._cmdline_cfg
        elif isinstance(self._cmdline_cfg, object) and not isinstance(self._cmdline_cfg, type(dummy)):
            cmdline_cfg = self._cmdline_cfg(default_cfg=self._default_cfg)(argv=argv)
        elif callable(self._cmdline_cfg):
            cmdline_cfg = self._cmdline_cfg(argv=argv, default_cfg=self._default_cfg)
        else:
            raise NotImplementedError

        # cfgfile can exist in cmdline,
        # but could also have been set in defaults
        cfgfile = cmdline_cfg.get("cfgfile", self._default_cfg.get("cfgfile"))
        if cfgfile is None:
            # build the search path if it's valid
            search_paths = self._default_cfg.get("cfgfile_search_paths")
            cfgname = self._default_cfg.get("cfgname")
            if search_paths and cfgname:
                search_paths = [e.format(cfgname=cfgname) for e in search_paths]
                cfgfile = which(cfgfile, expandpath(search_paths))

        cfgdata_file = _read(cfgfile) or {}

        # We merge in the inverse order of priority
        cfgdata = self._default_cfg
        cfgdata = deepmerge(cfgdata, cfgdata_file)
        cfgdata = deepmerge(cfgdata, cmdline_cfg)
        cfgdata = deepmerge(cfgdata, self._forced_cfg)
        return cfgdata


@define(kw_only=True, slots=False)
class ABCFlasketCli(abc.ABC, _DefaultCfgMixin):
    """
    Abstract base class to run a middleware.

    Parameters
    ----------
    default_cfg: dict, default: :meth:`flasket.defaults.default_configuration`

        Dictionary containing the defaults for the command line arguments in a inner
        ``server`` dict.
        Passed value will be merged with the default configuration.

        Will be passed to `cmdline_cfg` and `settings_cfg` if they are Callable.

    cmdline_cfg: any, default: None

        Dictionary, or Callable that returns a dictionary for the command line arguments.
        Defaults to None

        Will be passed to `settings_cfg` if the later is Callable.

    settings_cfg: any, default: :class:`flasket.cli.FlasketSettings`

        Dictionary, or Callable that returns a dictionary for the settings arguments.
        Defaults to :class:`flasket.cli.FlasketSettings`

    forced_cfg: dict, default: None

        Dictionary of settings to force after configuration generation.

        Will be passed to `settings_cfg` if the later is a Callable.
    """

    _cmdline_cfg: t.Any = field(default=None)
    _settings_cfg: t.Any = field(default=FlasketSettings)
    _forced_cfg: t.Dict = field(default=None)
    _options: t.Any = field(default=None)
    ctx: t.Any = field(default=suppress_traceback)

    @abc.abstractmethod
    def _run(self, *args, cfg: t.Dict, rootpath: str = None, **kwargs) -> None:
        """
        Run a Flasket middleware.

        Parameters
        ----------
        cfg: dict

            configuration dictionary to use

        rootpath: str, default: None

            path of root location: where the 'api', 'htdocs' and 'app' directories will be served.

            Current directory will be used if missing.
        """
        return

    def run(self, *args, argv: t.List[str] = None, rootpath: str = None, **kwargs) -> None:
        """
        Run a Flasket with automatic parsing of command line and configuration file.

        If `settings_cfg` is callable, then call it with `cmdline_cfg`, `default_cfg`, and `forced_cfg`. This
        will run :meth:`flasket.cli.FlasketSettings.__call__` which will parse the command line arguments, read
        the configuration file, and return a configuration dictionary.

        Otherwise, `settings_cfg` will be used as-is.

        Parameters
        ----------
        argv: list[str], default: None

            Uses :code:`sys.argv[1:]` if None

        rootpath: str, default: None

            path of root location: where the 'api', 'htdocs' and 'app' directories will be served.

        Raises
        ------
        SystemExit

            Function does not return
        """
        # pylint: disable=not-callable
        with self.ctx():
            # Empty/None settings have no sense since it'll
            # block the start of Flask/Gunicorn.
            cfg = {}
            if self._settings_cfg is None:
                cfg = self._default_cfg
            elif isinstance(self._settings_cfg, dict):
                cfg = self._settings_cfg
            elif isinstance(self._settings_cfg, object) and not isinstance(self._settings_cfg, type(dummy)):
                cfg = self._settings_cfg(
                    cmdline_cfg=self._cmdline_cfg,
                    default_cfg=self._default_cfg,
                    forced_cfg=self._forced_cfg,
                )(argv=argv)
            elif callable(self._settings_cfg):
                cfg = self._settings_cfg(
                    argv=argv,
                    cmdline_cfg=self._cmdline_cfg,
                    default_cfg=self._default_cfg,
                    forced_cfg=self._forced_cfg,
                )
            else:
                raise NotImplementedError

            # rootpath was probably passed by "__file__"
            if rootpath and os.path.isfile(rootpath):
                rootpath = os.path.dirname(rootpath)

            self._run(*args, cfg=cfg, rootpath=rootpath, **kwargs)
            sys.exit(0)


# pylint: disable=invalid-name
def FlasketCLIHelper(
    klass: "FlasketCLI",
    *,
    cfgname: str = None,
    description: str = None,
    options: t.Dict = None,
) -> "FlasketCLI":
    """
    Parameters
    ----------
    cfgname: str

        Name of the configuration file

    description: str

        Description to be used in argparse

    options: str

        Dictionnary of options

    """
    default_cfg = {"server": {}}
    if cfgname:
        default_cfg["cfgname"] = cfgname
    if description:
        default_cfg["description"] = description
    return klass(default_cfg=default_cfg, options=options)
