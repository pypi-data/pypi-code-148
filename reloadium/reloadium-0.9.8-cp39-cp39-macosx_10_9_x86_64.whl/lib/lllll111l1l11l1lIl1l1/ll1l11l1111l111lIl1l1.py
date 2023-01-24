from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.l1lll1111l11ll1lIl1l1 import l1lll1l1ll1ll1llIl1l1
from reloadium.lib.lllll111l1l11l1lIl1l1.ll1ll11l11l1l11lIl1l1 import l111l11ll1l111llIl1l1
from reloadium.corium.l1lll1ll11ll1lllIl1l1 import lll1111l1l1l1l1lIl1l1, l1l1lll11ll1lll1Il1l1, l111l11l1l1l1l1lIl1l1, l1l1ll1l1lll11l1Il1l1
from reloadium.corium.llll1l1llll1llllIl1l1 import lllll1l11l11ll1lIl1l1
from reloadium.corium.l111ll1llll1llllIl1l1 import l1l1lllll111lll1Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass
else:
    from reloadium.vendored.dataclasses import dataclass


@dataclass(**l1l1ll1l1lll11l1Il1l1)
class ll1l1lll1111lll1Il1l1(l111l11l1l1l1l1lIl1l1):
    l1ll1111111ll11lIl1l1 = 'FlaskApp'

    @classmethod
    def lll11111l11l111lIl1l1(lll11l1lll1llll1Il1l1, lll1l111l1l11lllIl1l1: lllll1l11l11ll1lIl1l1.l1lll1l1lllll11lIl1l1, l1l111l1l1l1lll1Il1l1: Any, l1llllll1l111l1lIl1l1: lll1111l1l1l1l1lIl1l1) -> bool:
        import flask

        if (isinstance(l1l111l1l1l1lll1Il1l1, flask.Flask)):
            return True

        return False

    def ll1lll11l11l1l11Il1l1(ll11l1llll1ll1l1Il1l1) -> bool:
        return True

    @classmethod
    def l11l1llll1ll1l11Il1l1(lll11l1lll1llll1Il1l1) -> int:
        return (super().l11l1llll1ll1l11Il1l1() + 10)


@dataclass(**l1l1ll1l1lll11l1Il1l1)
class l1lll1111llll1llIl1l1(l111l11l1l1l1l1lIl1l1):
    l1ll1111111ll11lIl1l1 = 'Request'

    @classmethod
    def lll11111l11l111lIl1l1(lll11l1lll1llll1Il1l1, lll1l111l1l11lllIl1l1: lllll1l11l11ll1lIl1l1.l1lll1l1lllll11lIl1l1, l1l111l1l1l1lll1Il1l1: Any, l1llllll1l111l1lIl1l1: lll1111l1l1l1l1lIl1l1) -> bool:
        if (repr(l1l111l1l1l1lll1Il1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def ll1lll11l11l1l11Il1l1(ll11l1llll1ll1l1Il1l1) -> bool:
        return True

    @classmethod
    def l11l1llll1ll1l11Il1l1(lll11l1lll1llll1Il1l1) -> int:

        return int(10000000000.0)


@dataclass
class l111111ll1ll1111Il1l1(l111l11ll1l111llIl1l1):
    l11111l1l1ll1111Il1l1 = 'Flask'

    @contextmanager
    def l11ll1lll11ll1l1Il1l1(ll11l1llll1ll1l1Il1l1, ll11l11111ll11llIl1l1: str, l1llll1ll11111llIl1l1: Dict[str, Any]) -> Generator[Tuple[str, Dict[str, Any]], None, None]:






        from flask import Flask as FlaskLib 

        def ll1llll1llll1111Il1l1(*l1llll1l1lll1lllIl1l1: Any, **lll11lll1lll1l1lIl1l1: Any) -> Any:
            def ll11ll1l11ll1l11Il1l1(l1111lll11llll1lIl1l1: Any) -> Any:
                return l1111lll11llll1lIl1l1

            return ll11ll1l11ll1l11Il1l1

        l1lll11ll1ll1l11Il1l1 = FlaskLib.route
        FlaskLib.route = ll1llll1llll1111Il1l1  # type: ignore

        try:
            yield (ll11l11111ll11llIl1l1, l1llll1ll11111llIl1l1, )
        finally:
            FlaskLib.route = l1lll11ll1ll1l11Il1l1  # type: ignore

    def lllllll1l1l1111lIl1l1(ll11l1llll1ll1l1Il1l1) -> List[Type[l1l1lll11ll1lll1Il1l1]]:
        return [ll1l1lll1111lll1Il1l1, l1lll1111llll1llIl1l1]

    def llll11llll1llll1Il1l1(ll11l1llll1ll1l1Il1l1, l11l1lll11l1l1l1Il1l1: types.ModuleType) -> None:
        if (ll11l1llll1ll1l1Il1l1.l1l1ll111lll1ll1Il1l1(l11l1lll11l1l1l1Il1l1, 'flask.app')):
            ll11l1llll1ll1l1Il1l1.l111l1ll11ll1lllIl1l1()
            ll11l1llll1ll1l1Il1l1.ll111llllll11l11Il1l1()
            ll11l1llll1ll1l1Il1l1.l1ll1ll1llllllllIl1l1()

        if (ll11l1llll1ll1l1Il1l1.l1l1ll111lll1ll1Il1l1(l11l1lll11l1l1l1Il1l1, 'flask.cli')):
            ll11l1llll1ll1l1Il1l1.lll11ll111ll1ll1Il1l1()

    def l111l1ll11ll1lllIl1l1(ll11l1llll1ll1l1Il1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        l11lll11lll11111Il1l1 = werkzeug.serving.run_simple

        def l11ll1111lll1111Il1l1(*l1llll1l1lll1lllIl1l1: Any, **lll11lll1lll1l1lIl1l1: Any) -> Any:
            with l1lll1l1ll1ll1llIl1l1():
                l1111111111lllllIl1l1 = lll11lll1lll1l1lIl1l1.get('port')
                if ( not l1111111111lllllIl1l1):
                    l1111111111lllllIl1l1 = l1llll1l1lll1lllIl1l1[1]

                ll11l1llll1ll1l1Il1l1.l1l11l1ll111111lIl1l1 = ll11l1llll1ll1l1Il1l1.ll1111ll111l11llIl1l1(l1111111111lllllIl1l1)
                if (env.page_reload_on_start):
                    ll11l1llll1ll1l1Il1l1.l1l11l1ll111111lIl1l1.l111l1ll11ll1l11Il1l1(1.0)
            l11lll11lll11111Il1l1(*l1llll1l1lll1lllIl1l1, **lll11lll1lll1l1lIl1l1)

        l1l1lllll111lll1Il1l1.ll1111l11lll1l11Il1l1(werkzeug.serving, 'run_simple', l11ll1111lll1111Il1l1)
        l1l1lllll111lll1Il1l1.ll1111l11lll1l11Il1l1(flask.cli, 'run_simple', l11ll1111lll1111Il1l1)

    def l1ll1ll1llllllllIl1l1(ll11l1llll1ll1l1Il1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        l11lll11lll11111Il1l1 = flask.app.Flask.__init__

        def l11ll1111lll1111Il1l1(l1lllll11lll11llIl1l1: Any, *l1llll1l1lll1lllIl1l1: Any, **lll11lll1lll1l1lIl1l1: Any) -> Any:
            l11lll11lll11111Il1l1(l1lllll11lll11llIl1l1, *l1llll1l1lll1lllIl1l1, **lll11lll1lll1l1lIl1l1)
            with l1lll1l1ll1ll1llIl1l1():
                l1lllll11lll11llIl1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        l1l1lllll111lll1Il1l1.ll1111l11lll1l11Il1l1(flask.app.Flask, '__init__', l11ll1111lll1111Il1l1)

    def ll111llllll11l11Il1l1(ll11l1llll1ll1l1Il1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        l11lll11lll11111Il1l1 = waitress.serve


        def l11ll1111lll1111Il1l1(*l1llll1l1lll1lllIl1l1: Any, **lll11lll1lll1l1lIl1l1: Any) -> Any:
            with l1lll1l1ll1ll1llIl1l1():
                l1111111111lllllIl1l1 = lll11lll1lll1l1lIl1l1.get('port')
                if ( not l1111111111lllllIl1l1):
                    l1111111111lllllIl1l1 = int(l1llll1l1lll1lllIl1l1[1])

                l1111111111lllllIl1l1 = int(l1111111111lllllIl1l1)

                ll11l1llll1ll1l1Il1l1.l1l11l1ll111111lIl1l1 = ll11l1llll1ll1l1Il1l1.ll1111ll111l11llIl1l1(l1111111111lllllIl1l1)
                if (env.page_reload_on_start):
                    ll11l1llll1ll1l1Il1l1.l1l11l1ll111111lIl1l1.l111l1ll11ll1l11Il1l1(1.0)

            l11lll11lll11111Il1l1(*l1llll1l1lll1lllIl1l1, **lll11lll1lll1l1lIl1l1)

        l1l1lllll111lll1Il1l1.ll1111l11lll1l11Il1l1(waitress, 'serve', l11ll1111lll1111Il1l1)

    def lll11ll111ll1ll1Il1l1(ll11l1llll1ll1l1Il1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        lll111lll111lll1Il1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        lll111lll111lll1Il1l1 = lll111lll111lll1Il1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(lll111lll111lll1Il1l1, cli.__dict__)

    def l1ll1l11l1l1l11lIl1l1(ll11l1llll1ll1l1Il1l1) -> None:
        super().l1ll1l11l1l1l11lIl1l1()
        import flask.app

        l11lll11lll11111Il1l1 = flask.app.Flask.dispatch_request

        def l11ll1111lll1111Il1l1(*l1llll1l1lll1lllIl1l1: Any, **lll11lll1lll1l1lIl1l1: Any) -> Any:
            l1lll11ll111lll1Il1l1 = l11lll11lll11111Il1l1(*l1llll1l1lll1lllIl1l1, **lll11lll1lll1l1lIl1l1)

            if ( not ll11l1llll1ll1l1Il1l1.l1l11l1ll111111lIl1l1):
                return l1lll11ll111lll1Il1l1

            if (isinstance(l1lll11ll111lll1Il1l1, str)):
                l1l1111l1ll1llllIl1l1 = ll11l1llll1ll1l1Il1l1.l1l11l1ll111111lIl1l1.lll1l1l11ll11l1lIl1l1(l1lll11ll111lll1Il1l1)
                return l1l1111l1ll1llllIl1l1
            elif ((isinstance(l1lll11ll111lll1Il1l1, flask.app.Response) and 'text/html' in l1lll11ll111lll1Il1l1.content_type)):
                l1lll11ll111lll1Il1l1.data = ll11l1llll1ll1l1Il1l1.l1l11l1ll111111lIl1l1.lll1l1l11ll11l1lIl1l1(l1lll11ll111lll1Il1l1.data.decode('utf-8')).encode('utf-8')
                return l1lll11ll111lll1Il1l1
            else:
                return l1lll11ll111lll1Il1l1

        flask.app.Flask.dispatch_request = l11ll1111lll1111Il1l1  # type: ignore
