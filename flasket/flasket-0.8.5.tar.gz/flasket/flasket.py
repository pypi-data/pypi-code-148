"""
Description
-----------

Main application. It handles returning the WSGI application,
but also returning the potential services it can connect to and use.

On the OpenAPI side, it handles merging multiple yaml files into a single
specification before loading it.

Classes
-------

Flasket
^^^^^^^

.. autoclass:: Flasket
  :show-inheritance:
  :members: baseurl, clients, config, current_app, debug, flask, backends, host, logger, make_response, port, redirect, render_template, request, rootpath, session, sitename,

"""
import logging
import os
import random
import string
import sys
import typing as t
import weakref

from attrs import define, field
from flask import Flask, current_app
from flask import g as flask_g
from flask_gordon.middleware import BeforeFirstCall, Dispatcher
from werkzeug.middleware.proxy_fix import ProxyFix as ProxyMiddleware

from .backends import ApiBackend, DashBackend, StaticBackend
from .logger import Logger
from .properties import BackendProperties

__all__: t.List[str] = [
    "Flasket",
]


@BackendProperties.post_init
@define(kw_only=True, slots=False)
class Flasket(BackendProperties):
    #: Root/Parent flasket application will be a reference to ourself
    _flasket = field(default=None, init=False)

    # Flask 'extensions'
    _celery = field(default=None, init=False)

    # Flask 'backends'
    _backends: t.Dict = field(default=None)
    _backends_cls = field(default=[DashBackend, ApiBackend, StaticBackend], init=False)

    # Class variables have most properties defined
    # in FlasketProperties
    _cfg = field(default=None)
    _clients = field(default=None, init=False)

    # Paths
    _rootpath = field(default=None)

    # Flags
    _debug = field(default=False, init=False)

    # --------------------------------------------------------------------------
    def __init_locals(self) -> None:
        # Fixup variables
        self._cfg = self._cfg or {}
        self._options = self._options or {}

    def __init_debug_flags(self) -> None:
        """
        Set the class variables to the values that were passed on by configuration.
        If debug is on, set the logger level
        """
        self._debug = self.config["server"].get("debug", False)
        if self.debug:
            self.logger.setLevel(logging.DEBUG)

    def __init_rootpath(self) -> None:
        def add_to_syspath(path):
            if path not in sys.path:
                self.logger.info(f'Adding path "{path}" to sys.path to enable dynamic loading...')
                sys.path.insert(0, path)

        rootpath = self._rootpath or os.getcwd()
        self._rootpath = os.path.abspath(rootpath)
        if not os.path.exists(self._rootpath) or not os.path.isdir(self._rootpath):
            self.logger.error(f'Root path directory "{self._rootpath}" does not exist.')
            sys.exit(1)
        self.logger.info(f'Using root path "{self._rootpath}" for dynamic loading.')
        add_to_syspath(self._rootpath)

    def __init_flask(self) -> None:
        # Initialize a Flask app with no static nor template folders
        self.logger.info("Initializing root Flask application...")
        self._flask = Flask(__name__, static_folder=None, template_folder=None)
        # Add 'flasket' to Flask app, so it's available via current_app
        self._flask.flasket = weakref.proxy(self)

    def __init_defaults(self) -> None:
        # Configuration comes from several locations:
        # - the command line arguments,
        # - the configuration file
        # - defaults
        #
        # Flask is also very flexible to where settings can come from.
        #
        # The most important variables, mostly to start/pre-configure the service
        # have already been set
        #
        # Set some new defaults
        self.flask.config["JSON_SORT_KEYS"] = False
        # FIXME modify to be options
        self.flask.config["TEMPLATES_AUTO_RELOAD"] = os.getenv("TEMPLATES_AUTO_RELOAD")
        self.flask.config["EXPLAIN_TEMPLATE_LOADING"] = os.getenv("EXPLAIN_TEMPLATE_LOADING")

    def __init_config(self) -> None:
        server = self.config.get("flask") or {}
        for key, _ in self.flask.config.items():
            lkey = key.lower()
            if lkey in server:
                self.flask.config[key] = server[lkey]

    def __init_secret(self) -> None:
        # Handle the secret session key if missing
        secret_key = self.flask.config["SECRET_KEY"]
        if not secret_key:
            self.flask.config["SECRET_KEY"] = "".join(random.choices(string.ascii_letters, k=20))
            self.logger.warning("Generated a random secret session key")

    def __init_backends(self) -> None:
        # Load all backends
        # For every backend get option[name] for that backend
        self._backends = {}
        for cls in self._backends_cls:  # pylint: disable=not-an-iterable
            options = self._options.get(cls.name()) or {}
            backend = cls(flasket=weakref.proxy(self), options=options)
            self._backends[backend.prefix] = backend

    def __init_middleware(self) -> None:
        # Queue the middlewares
        middleware = Dispatcher(self._backends["/"], self._backends)
        proxy = self.config["server"].get("proxy", {})
        if proxy:
            middleware = ProxyMiddleware(middleware, **proxy)
        middleware = BeforeFirstCall(middleware, self._before_first_call)
        self.flask._wsgi_app = self.flask.wsgi_app
        self.flask.wsgi_app = middleware

    def __attrs_post_init__(self) -> None:
        """
        Lorem ipsum sit dolor amet
        """
        # Set a ref to self
        self._flasket = weakref.proxy(self)

        Logger.configure()
        self.logger.info("Creating a new Flasket application...")

        self.__init_locals()
        self.__init_debug_flags()
        self.__init_rootpath()
        self.__init_flask()
        self.__init_defaults()
        self.__init_config()

        # https://flask.palletsprojects.com/en/2.2.x/config/
        self.flask.config["DEBUG"] = self.config["server"]["debug"]

        self.__init_secret()
        self.__init_backends()
        self.__init_middleware()

        # Load dynamic client loader
        ## self._clients = ClientFactory(flasket=weakref.proxy(self))
        # Load all jinja2 templates
        ### self.logger.info("Loading Jinja2 templates...")
        ### for name, fn in g_template_global.items():
        ###     self.logger.debug(f'Loading Jinja2 template "{name}"...')
        ###     self.add_template_global(fn, name)

    def _register_fake_route(self, handler):
        # And add 'flasket' to Flask app, so it's available via current_app
        handler.flask.flasket = weakref.proxy(self)
        handler.flask.before_request(Flasket._before_request)
        handler.flask.after_request(Flasket._after_request)

    @staticmethod
    def _before_first_call() -> None:
        Logger.disable()

    @staticmethod
    def _before_request() -> None:
        # Inject some variables available to templates
        flasket = current_app.flasket
        flask_g.flasket = flasket

    @staticmethod
    def _after_request(response) -> None:
        # This method is called after after_request, and for all routes
        flasket = current_app.flasket

        # Log the request
        Logger.log_request(flasket.request, response)
        return response

    # --------------------------------------------------------------------------
    def add_template_global(self, fn, name=None):
        for _, handler in self._backends.items():
            handler.flask.add_template_global(fn, name)

    # --------------------------------------------------------------------------
    # Properties
    @property
    def sitename(self) -> str:
        """
        Return combination of network host and port
        """
        if self.port == 80:
            return f"http://{self.host}"
        return f"http://{self.host}:{self.port}"

    @property
    def host(self) -> str:
        """
        Network hosts on which Flasket is listening on.
        """
        return self.config["server"]["listen"]

    @property
    def port(self) -> int:
        """
        Network post on which Flasket is listening on.
        """
        return self.config["server"]["port"]

    @property
    def baseurl(self) -> str:
        """
        Returns baseurl "{scheme}://{netloc}"
        """
        baseurl = self.config["server"].get("baseurl", None)
        if baseurl:
            return baseurl
        return self.sitename

    # --------------------------------------------------------------------------
    def pre_run(self) -> t.Any:
        if self._celery:
            self._celery.pre_run()

    def run(self) -> t.Any:
        self.pre_run()
        return self.flask.run(host=self.host, port=self.port, debug=self.debug, use_reloader=False)

    @property
    def backends(self) -> t.Dict[str, "Backend"]:
        """
        Returns array of backends
        """
        return self._backends
