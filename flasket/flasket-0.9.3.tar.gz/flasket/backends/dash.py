import os
import typing as t

from boltons.fileutils import iter_find_files
from dash import Dash, html
from dash import register_page as dash_register_page

from ._backend import Backend
###
###
###def app_layout(layout):
###    if DashBackend._dash:
###        DashBackend._dash.layout = layout
###        DashBackend.layout = layout
###    else:
###        DashBackend.layout = layout
###
###
###def callback(*args, **kwargs):
###    def wrapper(fn):
###        DashBackend._callbacks += [(fn, args, kwargs)]
###
###    if DashBackend._dash:
###        print("Setting callback on live dash app xxx")
###    else:
###        print("Setting callback on empty dash app xxx")
###    return wrapper
###
###
###def register_page(*args, **kwargs):
###    # Nuke the app prefix
###    # prefix = DashBackend._prefix()
###    # path = kwargs["path"]
###    # path = path[len(prefix):]
###    # kwargs["path"] = path
###    DashBackend._registered_pages += [(args, kwargs)]
###
dash = None

class DashBackend(Backend):
    _callbacks = []
    _registered_pages = []

    @staticmethod
    def init_app(flasket, rootpath, options=None) -> "DashBackend":
        return DashBackend(flasket, rootpath, options)

    @staticmethod
    def name() -> str:
        return "dash"

    @property
    def prefix(self) -> str:
        return "/app"

    @staticmethod
    def _prefix() -> str:
        return "/app"

    def __init__(self, flasket, rootpath, options=None):
        super().__init__(flasket, rootpath)

        self._init_rootpath(rootpath)
        self._init_dash(options)
        self._init_app_files()
        self._init_decorators()
        self._flasket._register_backend(self)
        self._configured = True

    def _init_rootpath(self, rootpath: str) -> None:
        rootpath = os.path.join(rootpath, "app")
        if not os.path.exists(rootpath):
            self.logger.warning('Directory "app" in root path does not exist.')
        self._rootpath = rootpath

    def _init_dash(self, options: t.Dict[str, t.Any]) -> None:
        # Some settings can't be used together
        use_pages = options.get("use_pages", False)
        if use_pages:
            pages_folder = options.get("pages", "")
        else:
            pages_folder = None

        global dash
        dash = Dash(
            __name__,
            # url_base_pathname="/app/",
            # requests_pathname_prefix="/app/",
            routes_pathname_prefix="/app/",
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
            pages_folder=pages_folder,
            # plugins=None,
            prevent_initial_callbacks=options.get("prevent_initial_callbacks", False),
            # serve_locally=True,
            # server=True,
            # show_undo_redo=False,
            suppress_callback_exceptions=options.get("suppress_callback_exceptions", False),
            title=options.get("title", "Flasket"),
            update_title=options.get("update_title", ""),
            use_pages=use_pages,
        )

        self._flask = dash.server
        self.logger.info(f"Aplication is available at: {self.flasket.sitename}/app/")

    def _init_app_files(self) -> None:
        files = iter_find_files(self._rootpath, "*.py")
        files = sorted(set(files))

        # TODO: Load __init__.py only once, that means
        # don't load it if files exist next to it.
        modules = []
        dirname = self._flasket.rootpath.split("/")[-1]
        for file in files:
            file = os.path.relpath(file, self._flasket.rootpath)
            # if os.path.basename(file) == "__init__.py":
            #     continue
            file = file[:-3]
            file = file.replace("/", ".")
            file = dirname + "." + file
            modules += [file]

        for module in modules:
            __import__(module, globals(), locals())
            ###assert callable(
            ###    app_layout,
            ###), f"error: app_layout was set to a variable in module '{module}'. Use it as a function: app_layout(html...)"

    def _init_decorators(self):
        def callback_wrapper(cb_fn, cb_args, cb_kwargs):
            @self._dash.callback(*cb_args, **cb_kwargs)
            def wrapper(*args, **kwargs):
                print("Setting callback on saved dash app")
                return cb_fn(*args, **kwargs)

        ###for fn in self._callbacks:
        ###    callback_wrapper(fn[0], fn[1], fn[2])

        ###for args in self._registered_pages:
        ###    dash_register_page(*args[0], **args[1])

    def __call__(self, environ: dict, start_response):
        return self._flask(environ, start_response)
