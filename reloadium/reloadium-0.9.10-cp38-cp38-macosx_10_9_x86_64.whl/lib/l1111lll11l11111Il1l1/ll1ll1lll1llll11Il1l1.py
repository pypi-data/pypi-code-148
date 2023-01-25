from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.llll11111l111lllIl1l1 import l111ll11ll11l1l1Il1l1
from reloadium.lib.l1111lll11l11111Il1l1.l111llll1llll1l1Il1l1 import lllllllll1l11111Il1l1
from reloadium.corium.lll11111lll1ll1lIl1l1 import l1ll111ll1l11l11Il1l1, l1l111111l111111Il1l1, ll111111l111llllIl1l1, l111llll1ll1ll1lIl1l1
from reloadium.corium.lll1l1lllll111l1Il1l1 import ll1ll11l11l11lllIl1l1
from reloadium.corium.l11lllll1ll1l11lIl1l1 import l1l1l1l11lll1l1lIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass
else:
    from reloadium.vendored.dataclasses import dataclass


@dataclass(**l111llll1ll1ll1lIl1l1)
class l1llll111ll1111lIl1l1(ll111111l111llllIl1l1):
    lllll1l1111111llIl1l1 = 'FlaskApp'

    @classmethod
    def ll11llll1111111lIl1l1(llll11ll11l1lll1Il1l1, ll1lll1l11l111llIl1l1: ll1ll11l11l11lllIl1l1.l1llllll111lllllIl1l1, l111ll1ll1l1ll1lIl1l1: Any, l1l1l1ll1ll1l1llIl1l1: l1ll111ll1l11l11Il1l1) -> bool:
        import flask

        if (isinstance(l111ll1ll1l1ll1lIl1l1, flask.Flask)):
            return True

        return False

    def ll1llll111llll11Il1l1(ll1l1l1l11l1l11lIl1l1) -> bool:
        return True

    @classmethod
    def llll1ll111lll111Il1l1(llll11ll11l1lll1Il1l1) -> int:
        return (super().llll1ll111lll111Il1l1() + 10)


@dataclass(**l111llll1ll1ll1lIl1l1)
class l11l111111lll1l1Il1l1(ll111111l111llllIl1l1):
    lllll1l1111111llIl1l1 = 'Request'

    @classmethod
    def ll11llll1111111lIl1l1(llll11ll11l1lll1Il1l1, ll1lll1l11l111llIl1l1: ll1ll11l11l11lllIl1l1.l1llllll111lllllIl1l1, l111ll1ll1l1ll1lIl1l1: Any, l1l1l1ll1ll1l1llIl1l1: l1ll111ll1l11l11Il1l1) -> bool:
        if (repr(l111ll1ll1l1ll1lIl1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def ll1llll111llll11Il1l1(ll1l1l1l11l1l11lIl1l1) -> bool:
        return True

    @classmethod
    def llll1ll111lll111Il1l1(llll11ll11l1lll1Il1l1) -> int:

        return int(10000000000.0)


@dataclass
class llll1l1l111lll11Il1l1(lllllllll1l11111Il1l1):
    ll11lll1ll1l1l11Il1l1 = 'Flask'

    @contextmanager
    def ll1111ll11lll1llIl1l1(ll1l1l1l11l1l11lIl1l1) -> Generator[None, None, None]:




        from flask import Flask as FlaskLib 

        def ll11lllll11ll1l1Il1l1(*ll111l1ll1l1llllIl1l1: Any, **l1111l1l1ll1l1llIl1l1: Any) -> Any:
            def ll1l11llll111l1lIl1l1(ll1lll1lll1ll11lIl1l1: Any) -> Any:
                return ll1lll1lll1ll11lIl1l1

            return ll1l11llll111l1lIl1l1

        l1ll1lllllllll11Il1l1 = FlaskLib.route
        FlaskLib.route = ll11lllll11ll1l1Il1l1  # type: ignore

        try:
            yield 
        finally:
            FlaskLib.route = l1ll1lllllllll11Il1l1  # type: ignore

    def ll1l1llllll1l11lIl1l1(ll1l1l1l11l1l11lIl1l1) -> List[Type[l1l111111l111111Il1l1]]:
        return [l1llll111ll1111lIl1l1, l11l111111lll1l1Il1l1]

    def l1lll1lll1111lllIl1l1(ll1l1l1l11l1l11lIl1l1, l111l111111l1111Il1l1: types.ModuleType) -> None:
        if (ll1l1l1l11l1l11lIl1l1.l1lll1lll1l1lll1Il1l1(l111l111111l1111Il1l1, 'flask.app')):
            ll1l1l1l11l1l11lIl1l1.ll1llll111111111Il1l1()
            ll1l1l1l11l1l11lIl1l1.l1lll1ll1111l1l1Il1l1()
            ll1l1l1l11l1l11lIl1l1.l1ll1l11l1lll11lIl1l1()

        if (ll1l1l1l11l1l11lIl1l1.l1lll1lll1l1lll1Il1l1(l111l111111l1111Il1l1, 'flask.cli')):
            ll1l1l1l11l1l11lIl1l1.l1111l11ll1ll1llIl1l1()

    def ll1llll111111111Il1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        lll11ll1l11ll111Il1l1 = werkzeug.serving.run_simple

        def l11lll1l1l1l1ll1Il1l1(*ll111l1ll1l1llllIl1l1: Any, **l1111l1l1ll1l1llIl1l1: Any) -> Any:
            with l111ll11ll11l1l1Il1l1():
                l11ll1ll1l1111l1Il1l1 = l1111l1l1ll1l1llIl1l1.get('port')
                if ( not l11ll1ll1l1111l1Il1l1):
                    l11ll1ll1l1111l1Il1l1 = ll111l1ll1l1llllIl1l1[1]

                ll1l1l1l11l1l11lIl1l1.ll1lll111l11l1llIl1l1 = ll1l1l1l11l1l11lIl1l1.l11lll11l1111l1lIl1l1(l11ll1ll1l1111l1Il1l1)
                if (env.page_reload_on_start):
                    ll1l1l1l11l1l11lIl1l1.ll1lll111l11l1llIl1l1.l111ll1ll1l1lll1Il1l1(1.0)
            lll11ll1l11ll111Il1l1(*ll111l1ll1l1llllIl1l1, **l1111l1l1ll1l1llIl1l1)

        l1l1l1l11lll1l1lIl1l1.ll11l1l1l111ll11Il1l1(werkzeug.serving, 'run_simple', l11lll1l1l1l1ll1Il1l1)
        l1l1l1l11lll1l1lIl1l1.ll11l1l1l111ll11Il1l1(flask.cli, 'run_simple', l11lll1l1l1l1ll1Il1l1)

    def l1ll1l11l1lll11lIl1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        lll11ll1l11ll111Il1l1 = flask.app.Flask.__init__

        def l11lll1l1l1l1ll1Il1l1(l1lll11lll1lllllIl1l1: Any, *ll111l1ll1l1llllIl1l1: Any, **l1111l1l1ll1l1llIl1l1: Any) -> Any:
            lll11ll1l11ll111Il1l1(l1lll11lll1lllllIl1l1, *ll111l1ll1l1llllIl1l1, **l1111l1l1ll1l1llIl1l1)
            with l111ll11ll11l1l1Il1l1():
                l1lll11lll1lllllIl1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        l1l1l1l11lll1l1lIl1l1.ll11l1l1l111ll11Il1l1(flask.app.Flask, '__init__', l11lll1l1l1l1ll1Il1l1)

    def l1lll1ll1111l1l1Il1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        lll11ll1l11ll111Il1l1 = waitress.serve


        def l11lll1l1l1l1ll1Il1l1(*ll111l1ll1l1llllIl1l1: Any, **l1111l1l1ll1l1llIl1l1: Any) -> Any:
            with l111ll11ll11l1l1Il1l1():
                l11ll1ll1l1111l1Il1l1 = l1111l1l1ll1l1llIl1l1.get('port')
                if ( not l11ll1ll1l1111l1Il1l1):
                    l11ll1ll1l1111l1Il1l1 = int(ll111l1ll1l1llllIl1l1[1])

                l11ll1ll1l1111l1Il1l1 = int(l11ll1ll1l1111l1Il1l1)

                ll1l1l1l11l1l11lIl1l1.ll1lll111l11l1llIl1l1 = ll1l1l1l11l1l11lIl1l1.l11lll11l1111l1lIl1l1(l11ll1ll1l1111l1Il1l1)
                if (env.page_reload_on_start):
                    ll1l1l1l11l1l11lIl1l1.ll1lll111l11l1llIl1l1.l111ll1ll1l1lll1Il1l1(1.0)

            lll11ll1l11ll111Il1l1(*ll111l1ll1l1llllIl1l1, **l1111l1l1ll1l1llIl1l1)

        l1l1l1l11lll1l1lIl1l1.ll11l1l1l111ll11Il1l1(waitress, 'serve', l11lll1l1l1l1ll1Il1l1)

    def l1111l11ll1ll1llIl1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        l11l1lllll1l11l1Il1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        l11l1lllll1l11l1Il1l1 = l11l1lllll1l11l1Il1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(l11l1lllll1l11l1Il1l1, cli.__dict__)

    def l1111lll11l1111lIl1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        super().l1111lll11l1111lIl1l1()
        import flask.app

        lll11ll1l11ll111Il1l1 = flask.app.Flask.dispatch_request

        def l11lll1l1l1l1ll1Il1l1(*ll111l1ll1l1llllIl1l1: Any, **l1111l1l1ll1l1llIl1l1: Any) -> Any:
            ll1111llllllllllIl1l1 = lll11ll1l11ll111Il1l1(*ll111l1ll1l1llllIl1l1, **l1111l1l1ll1l1llIl1l1)

            if ( not ll1l1l1l11l1l11lIl1l1.ll1lll111l11l1llIl1l1):
                return ll1111llllllllllIl1l1

            if (isinstance(ll1111llllllllllIl1l1, str)):
                lll1ll1111l1ll11Il1l1 = ll1l1l1l11l1l11lIl1l1.ll1lll111l11l1llIl1l1.l1l11ll11l1ll111Il1l1(ll1111llllllllllIl1l1)
                return lll1ll1111l1ll11Il1l1
            elif ((isinstance(ll1111llllllllllIl1l1, flask.app.Response) and 'text/html' in ll1111llllllllllIl1l1.content_type)):
                ll1111llllllllllIl1l1.data = ll1l1l1l11l1l11lIl1l1.ll1lll111l11l1llIl1l1.l1l11ll11l1ll111Il1l1(ll1111llllllllllIl1l1.data.decode('utf-8')).encode('utf-8')
                return ll1111llllllllllIl1l1
            else:
                return ll1111llllllllllIl1l1

        flask.app.Flask.dispatch_request = l11lll1l1l1l1ll1Il1l1  # type: ignore
