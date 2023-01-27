# pylint: disable=invalid-name
# pylint: disable=global-variable-not-assigned
# pylint: disable=global-statement
import os

from attrs import define, field
from dash import Dash, html

from ._backend import Backend

__all__ = []

_callbacks = []
_layout = html.Div()


def layout(fn):
    global _layout
    _layout = fn


def callback(*args, **kwargs):
    def wrapper(fn):
        global _callbacks
        _callbacks += [(fn, args, kwargs)]

    return wrapper


@Backend.post_init
@define(kw_only=True, slots=False)
class DashBackend(Backend):
    _dash: str = field(init=False, default=None)
    _dash_rootpath: str = field(init=False, default=None)

    @staticmethod
    def name() -> str:
        return "dash"

    @property
    def prefix(self) -> str:
        return "/app"

    def __attrs_post_init__(self) -> None:
        self._dash_rootpath = os.path.join(self.rootpath, "app")
        if not os.path.exists(self._dash_rootpath):
            self.logger.warning('Directory "app" in root path does not exist.')

        # FIXME
        self._dash = Dash(
            __name__,
            url_base_pathname="/app/",
            #
            assets_external_path=self._options.get("assets_external_path"),
            external_stylesheets=self._options.get("external_stylesheets"),
            pages_folder=self._options.get("pages"),
            prevent_initial_callbacks=self._options.get("prevent_initial_callbacks", True),
            suppress_callback_exceptions=self._options.get("suppress_callback_exceptions", False),
            update_title=self._options.get("update_title"),
            # assets_folder='assets',
            # assets_ignore='',
            # assets_url_path='assets',
            # background_callback_manager=None,
            # compress=None,
            # eager_loading=False,
            # external_scripts=None,
            # extra_hot_reload_paths=None,
            # include_assets_files=True,
            # long_callback_manager=None,
            # meta_tags=None,
            # plugins=None,
            # requests_pathname_prefix=None,
            # routes_pathname_prefix=None,
            # serve_locally=True,
            # server=True,
            # show_undo_redo=False,
            # title='Dash',
            # use_pages=False,
        )
        global _layout
        self._dash.layout = _layout

        def cell_var_wrapper(cb_fn, cb_args, cb_kwargs):
            @self._dash.callback(*cb_args, **cb_kwargs)
            def wrapper(*args, **kwargs):
                return cb_fn(*args, **kwargs)

        global _callbacks
        for callback in _callbacks:
            cell_var_wrapper(callback[0], callback[1], callback[2])

        self._flask = self._dash.server
        self.logger.info(f"Aplication is available at: {self.sitename}/app/")

    def __call__(self, environ: dict, start_response):
        return self._flask(environ, start_response)
