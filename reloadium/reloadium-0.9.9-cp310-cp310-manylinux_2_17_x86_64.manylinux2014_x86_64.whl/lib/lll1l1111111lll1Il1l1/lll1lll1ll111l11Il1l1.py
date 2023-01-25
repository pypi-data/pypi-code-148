from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.l1l1l1l111l1ll1lIl1l1 import ll11lll1ll1lll1lIl1l1
from reloadium.lib.lll1l1111111lll1Il1l1.ll11ll111l1111l1Il1l1 import ll11l1l11ll1lll1Il1l1
from reloadium.corium.l1l1llllllllllllIl1l1 import l1llll111l1ll11lIl1l1, ll1ll1ll1111l11lIl1l1, ll11l1l1111l11llIl1l1, ll1l1lll11l111l1Il1l1
from reloadium.corium.l1111llllll11111Il1l1 import l11l1111llll111lIl1l1
from reloadium.corium.ll11ll11l1111l11Il1l1 import l1ll11ll11111l1lIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass
else:
    from reloadium.vendored.dataclasses import dataclass


@dataclass(**ll1l1lll11l111l1Il1l1)
class l1l1lll1111l1lllIl1l1(ll11l1l1111l11llIl1l1):
    l1111llll11l1111Il1l1 = 'FlaskApp'

    @classmethod
    def l1l1ll1l1ll1lll1Il1l1(ll1l11lll111111lIl1l1, l1ll1l11l11l11l1Il1l1: l11l1111llll111lIl1l1.llll1l111l1l11l1Il1l1, lll1l1ll1l1l1111Il1l1: Any, l11l11l111ll1lllIl1l1: l1llll111l1ll11lIl1l1) -> bool:
        import flask

        if (isinstance(lll1l1ll1l1l1111Il1l1, flask.Flask)):
            return True

        return False

    def l1l1lllll1l11l1lIl1l1(l1111l111ll1l1llIl1l1) -> bool:
        return True

    @classmethod
    def l11ll1l1l111l1llIl1l1(ll1l11lll111111lIl1l1) -> int:
        return (super().l11ll1l1l111l1llIl1l1() + 10)


@dataclass(**ll1l1lll11l111l1Il1l1)
class lll11lll11ll11llIl1l1(ll11l1l1111l11llIl1l1):
    l1111llll11l1111Il1l1 = 'Request'

    @classmethod
    def l1l1ll1l1ll1lll1Il1l1(ll1l11lll111111lIl1l1, l1ll1l11l11l11l1Il1l1: l11l1111llll111lIl1l1.llll1l111l1l11l1Il1l1, lll1l1ll1l1l1111Il1l1: Any, l11l11l111ll1lllIl1l1: l1llll111l1ll11lIl1l1) -> bool:
        if (repr(lll1l1ll1l1l1111Il1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def l1l1lllll1l11l1lIl1l1(l1111l111ll1l1llIl1l1) -> bool:
        return True

    @classmethod
    def l11ll1l1l111l1llIl1l1(ll1l11lll111111lIl1l1) -> int:

        return int(10000000000.0)


@dataclass
class ll1111l1111111l1Il1l1(ll11l1l11ll1lll1Il1l1):
    l11ll1llllll1ll1Il1l1 = 'Flask'

    @contextmanager
    def l1lll1ll1l1l1111Il1l1(l1111l111ll1l1llIl1l1) -> Generator[None, None, None]:




        from flask import Flask as FlaskLib 

        def lll1l1l1lll11ll1Il1l1(*l11l111ll1ll1l11Il1l1: Any, **llll11l1l11l1111Il1l1: Any) -> Any:
            def ll1l1l11ll11llllIl1l1(l11ll11ll1llll11Il1l1: Any) -> Any:
                return l11ll11ll1llll11Il1l1

            return ll1l1l11ll11llllIl1l1

        lll1llll1111l11lIl1l1 = FlaskLib.route
        FlaskLib.route = lll1l1l1lll11ll1Il1l1  # type: ignore

        try:
            yield 
        finally:
            FlaskLib.route = lll1llll1111l11lIl1l1  # type: ignore

    def l11l1l111llllll1Il1l1(l1111l111ll1l1llIl1l1) -> List[Type[ll1ll1ll1111l11lIl1l1]]:
        return [l1l1lll1111l1lllIl1l1, lll11lll11ll11llIl1l1]

    def l1ll111lllllll1lIl1l1(l1111l111ll1l1llIl1l1, llll1ll1l1l11l1lIl1l1: types.ModuleType) -> None:
        if (l1111l111ll1l1llIl1l1.lll1ll1l1lll1lllIl1l1(llll1ll1l1l11l1lIl1l1, 'flask.app')):
            l1111l111ll1l1llIl1l1.l111llllll11l1llIl1l1()
            l1111l111ll1l1llIl1l1.l111lll1l11lllllIl1l1()
            l1111l111ll1l1llIl1l1.l111l1ll11llll11Il1l1()

        if (l1111l111ll1l1llIl1l1.lll1ll1l1lll1lllIl1l1(llll1ll1l1l11l1lIl1l1, 'flask.cli')):
            l1111l111ll1l1llIl1l1.l111lll111lll11lIl1l1()

    def l111llllll11l1llIl1l1(l1111l111ll1l1llIl1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        lll1l1l11lll11l1Il1l1 = werkzeug.serving.run_simple

        def l111ll1lllll111lIl1l1(*l11l111ll1ll1l11Il1l1: Any, **llll11l1l11l1111Il1l1: Any) -> Any:
            with ll11lll1ll1lll1lIl1l1():
                l1ll11lll1l1l1l1Il1l1 = llll11l1l11l1111Il1l1.get('port')
                if ( not l1ll11lll1l1l1l1Il1l1):
                    l1ll11lll1l1l1l1Il1l1 = l11l111ll1ll1l11Il1l1[1]

                l1111l111ll1l1llIl1l1.llll111l1ll1l111Il1l1 = l1111l111ll1l1llIl1l1.ll111l1lll11lll1Il1l1(l1ll11lll1l1l1l1Il1l1)
                if (env.page_reload_on_start):
                    l1111l111ll1l1llIl1l1.llll111l1ll1l111Il1l1.l1llll111ll11lllIl1l1(1.0)
            lll1l1l11lll11l1Il1l1(*l11l111ll1ll1l11Il1l1, **llll11l1l11l1111Il1l1)

        l1ll11ll11111l1lIl1l1.ll11lll11111l1llIl1l1(werkzeug.serving, 'run_simple', l111ll1lllll111lIl1l1)
        l1ll11ll11111l1lIl1l1.ll11lll11111l1llIl1l1(flask.cli, 'run_simple', l111ll1lllll111lIl1l1)

    def l111l1ll11llll11Il1l1(l1111l111ll1l1llIl1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        lll1l1l11lll11l1Il1l1 = flask.app.Flask.__init__

        def l111ll1lllll111lIl1l1(l1l1ll1ll1lllll1Il1l1: Any, *l11l111ll1ll1l11Il1l1: Any, **llll11l1l11l1111Il1l1: Any) -> Any:
            lll1l1l11lll11l1Il1l1(l1l1ll1ll1lllll1Il1l1, *l11l111ll1ll1l11Il1l1, **llll11l1l11l1111Il1l1)
            with ll11lll1ll1lll1lIl1l1():
                l1l1ll1ll1lllll1Il1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        l1ll11ll11111l1lIl1l1.ll11lll11111l1llIl1l1(flask.app.Flask, '__init__', l111ll1lllll111lIl1l1)

    def l111lll1l11lllllIl1l1(l1111l111ll1l1llIl1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        lll1l1l11lll11l1Il1l1 = waitress.serve


        def l111ll1lllll111lIl1l1(*l11l111ll1ll1l11Il1l1: Any, **llll11l1l11l1111Il1l1: Any) -> Any:
            with ll11lll1ll1lll1lIl1l1():
                l1ll11lll1l1l1l1Il1l1 = llll11l1l11l1111Il1l1.get('port')
                if ( not l1ll11lll1l1l1l1Il1l1):
                    l1ll11lll1l1l1l1Il1l1 = int(l11l111ll1ll1l11Il1l1[1])

                l1ll11lll1l1l1l1Il1l1 = int(l1ll11lll1l1l1l1Il1l1)

                l1111l111ll1l1llIl1l1.llll111l1ll1l111Il1l1 = l1111l111ll1l1llIl1l1.ll111l1lll11lll1Il1l1(l1ll11lll1l1l1l1Il1l1)
                if (env.page_reload_on_start):
                    l1111l111ll1l1llIl1l1.llll111l1ll1l111Il1l1.l1llll111ll11lllIl1l1(1.0)

            lll1l1l11lll11l1Il1l1(*l11l111ll1ll1l11Il1l1, **llll11l1l11l1111Il1l1)

        l1ll11ll11111l1lIl1l1.ll11lll11111l1llIl1l1(waitress, 'serve', l111ll1lllll111lIl1l1)

    def l111lll111lll11lIl1l1(l1111l111ll1l1llIl1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        ll1ll1111ll111l1Il1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        ll1ll1111ll111l1Il1l1 = ll1ll1111ll111l1Il1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(ll1ll1111ll111l1Il1l1, cli.__dict__)

    def l1l11l11l11111l1Il1l1(l1111l111ll1l1llIl1l1) -> None:
        super().l1l11l11l11111l1Il1l1()
        import flask.app

        lll1l1l11lll11l1Il1l1 = flask.app.Flask.dispatch_request

        def l111ll1lllll111lIl1l1(*l11l111ll1ll1l11Il1l1: Any, **llll11l1l11l1111Il1l1: Any) -> Any:
            l11llllll11l1l11Il1l1 = lll1l1l11lll11l1Il1l1(*l11l111ll1ll1l11Il1l1, **llll11l1l11l1111Il1l1)

            if ( not l1111l111ll1l1llIl1l1.llll111l1ll1l111Il1l1):
                return l11llllll11l1l11Il1l1

            if (isinstance(l11llllll11l1l11Il1l1, str)):
                l11111111llllll1Il1l1 = l1111l111ll1l1llIl1l1.llll111l1ll1l111Il1l1.l1111ll11ll1l11lIl1l1(l11llllll11l1l11Il1l1)
                return l11111111llllll1Il1l1
            elif ((isinstance(l11llllll11l1l11Il1l1, flask.app.Response) and 'text/html' in l11llllll11l1l11Il1l1.content_type)):
                l11llllll11l1l11Il1l1.data = l1111l111ll1l1llIl1l1.llll111l1ll1l111Il1l1.l1111ll11ll1l11lIl1l1(l11llllll11l1l11Il1l1.data.decode('utf-8')).encode('utf-8')
                return l11llllll11l1l11Il1l1
            else:
                return l11llllll11l1l11Il1l1

        flask.app.Flask.dispatch_request = l111ll1lllll111lIl1l1  # type: ignore
