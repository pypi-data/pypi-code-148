import os
import typing as t

from boltons.fileutils import iter_find_files
from dash import Dash, html

from ._backend import Backend


def layout(fn):
    DashBackend.layout = fn()


def callback(*args, **kwargs):
    def wrapper(fn):
        DashBackend._callbacks += [(fn, args, kwargs)]

    return wrapper


class DashBackend(Backend):
    layout = html.Div()
    _callbacks = []

    @staticmethod
    def init_app(flasket, rootpath, options=None) -> "DashBackend":
        return DashBackend(flasket, rootpath, options)

    @staticmethod
    def name() -> str:
        return "dash"

    @property
    def prefix(self) -> str:
        return "/app"

    def __init__(self, flasket, rootpath, options=None):
        super().__init__(flasket, rootpath)

        self._init_rootpath(rootpath)
        self._init_dash(options)
        self._init_app_files()
        self._init_callbacks()
        self._flasket._register_backend(self)

    def _init_rootpath(self, rootpath: str) -> None:
        rootpath = os.path.join(rootpath, "app")
        if not os.path.exists(rootpath):
            self.logger.warning('Directory "app" in root path does not exist.')
        self._rootpath = rootpath

    def _init_dash(self, options: t.Dict[str, t.Any]) -> None:
        self._dash = Dash(
            __name__,
            url_base_pathname="/app/",
            #
            assets_external_path=options.get("assets_external_path"),
            # assets_folder='assets',
            # assets_ignore='',
            # assets_url_path='assets',
            # background_callback_manager=None,
            # compress=None,
            # eager_loading=False,
            # external_scripts=None,
            external_stylesheets=options.get("external_stylesheets"),
            # extra_hot_reload_paths=None,
            # include_assets_files=True,
            # long_callback_manager=None,
            # meta_tags=None,
            pages_folder=options.get("pages"),
            # plugins=None,
            prevent_initial_callbacks=options.get("prevent_initial_callbacks", False),
            # requests_pathname_prefix=None,
            routes_pathname_prefix=None,
            # serve_locally=True,
            # server=True,
            # show_undo_redo=False,
            suppress_callback_exceptions=options.get("suppress_callback_exceptions", False),
            title=options.get("title", "Flasket"),
            update_title=options.get("update_title", ""),
            use_pages=options.get("use_pages"),
        )
        self._flask = self._dash.server
        self.logger.info(f"Aplication is available at: {self.flasket.sitename}/app/")

    def _init_app_files(self) -> None:
        files = iter_find_files(self._rootpath, "*.py")
        files = sorted(files)

        modules = []
        dirname = self._flasket.rootpath.split("/")[-1]
        for file in files:
            file = os.path.relpath(file, self._flasket.rootpath)
            if os.path.basename(file) == "__init__.py":
                continue
            file = file[:-3]
            file = file.replace("/", ".")
            file = dirname + "." + file
            modules += [file]

        for module in modules:
            __import__(module)

    def _init_callbacks(self):
        self._dash.layout = self.layout

        def cell_var_wrapper(cb_fn, cb_args, cb_kwargs):
            @self._dash.callback(*cb_args, **cb_kwargs)
            def wrapper(*args, **kwargs):
                return cb_fn(*args, **kwargs)

        for fn in self._callbacks:
            cell_var_wrapper(fn[0], fn[1], fn[2])

    def __call__(self, environ: dict, start_response):
        print("__call__(self, environ: dict, start_response)")
        return self._flask(environ, start_response)
