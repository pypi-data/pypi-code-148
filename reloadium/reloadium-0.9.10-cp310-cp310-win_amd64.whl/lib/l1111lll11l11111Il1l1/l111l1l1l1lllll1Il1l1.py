from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.llll11111l111lllIl1l1 import l111ll11ll11l1l1Il1l1
from reloadium.lib.l1111lll11l11111Il1l1.lll1llll111l11llIl1l1 import lllll1l11lll1111Il1l1
from reloadium.lib.l1111lll11l11111Il1l1.l111llll1llll1l1Il1l1 import lllllllll1l11111Il1l1
from reloadium.corium.lll11111lll1ll1lIl1l1 import lllll111ll11ll11Il1l1, l1ll111ll1l11l11Il1l1, l1l111111l111111Il1l1, ll111111l111llllIl1l1, l111llll1ll1ll1lIl1l1
from reloadium.corium.llll11lll1llllllIl1l1 import lllll111ll1l1111Il1l1
from reloadium.corium.lll1l1lllll111l1Il1l1 import ll1ll11l11l11lllIl1l1
from reloadium.corium.l11lllll1ll1l11lIl1l1 import l1l1l1l11lll1l1lIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from django.db import transaction
    from django.db.transaction import Atomic
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass(**l111llll1ll1ll1lIl1l1)
class l111l1ll1ll11lllIl1l1(ll111111l111llllIl1l1):
    lllll1l1111111llIl1l1 = 'Field'

    @classmethod
    def ll11llll1111111lIl1l1(llll11ll11l1lll1Il1l1, ll1lll1l11l111llIl1l1: ll1ll11l11l11lllIl1l1.l1llllll111lllllIl1l1, l111ll1ll1l1ll1lIl1l1: Any, l1l1l1ll1ll1l1llIl1l1: l1ll111ll1l11l11Il1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(l111ll1ll1l1ll1lIl1l1, 'field') and isinstance(l111ll1ll1l1ll1lIl1l1.field, Field))):
            return True

        return False

    def ll1111l111l1ll1lIl1l1(ll1l1l1l11l1l11lIl1l1, l11ll1l111111111Il1l1: l1l111111l111111Il1l1) -> bool:
        return True

    @classmethod
    def llll1ll111lll111Il1l1(llll11ll11l1lll1Il1l1) -> int:
        return 200


@dataclass(repr=False)
class l11111ll111111llIl1l1(lllll1l11lll1111Il1l1):
    ll1ll1l111ll1111Il1l1: "Atomic" = field(init=False)

    ll1111llll1l1111Il1l1: bool = field(init=False, default=False)

    def __post_init__(ll1l1l1l11l1l11lIl1l1) -> None:
        super().__post_init__()
        from django.db import transaction

        ll1l1l1l11l1l11lIl1l1.ll1ll1l111ll1111Il1l1 = transaction.atomic()
        ll1l1l1l11l1l11lIl1l1.ll1ll1l111ll1111Il1l1.__enter__()

    def l11ll1ll1ll1l1llIl1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        super().l11ll1ll1ll1l1llIl1l1()
        if (ll1l1l1l11l1l11lIl1l1.ll1111llll1l1111Il1l1):
            return 

        ll1l1l1l11l1l11lIl1l1.ll1111llll1l1111Il1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        ll1l1l1l11l1l11lIl1l1.ll1ll1l111ll1111Il1l1.__exit__(None, None, None)

    def l1l11111ll11ll11Il1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        super().l1l11111ll11ll11Il1l1()

        if (ll1l1l1l11l1l11lIl1l1.ll1111llll1l1111Il1l1):
            return 

        ll1l1l1l11l1l11lIl1l1.ll1111llll1l1111Il1l1 = True
        ll1l1l1l11l1l11lIl1l1.ll1ll1l111ll1111Il1l1.__exit__(None, None, None)

    def __repr__(ll1l1l1l11l1l11lIl1l1) -> str:
        return 'DbMemento'


@dataclass
class l11llll11ll1ll11Il1l1(lllllllll1l11111Il1l1):
    ll11lll1ll1l1l11Il1l1 = 'Django'

    l1111ll1l111ll11Il1l1: Optional[int] = field(init=False)
    llll1l1l111llll1Il1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    def __post_init__(ll1l1l1l11l1l11lIl1l1) -> None:
        super().__post_init__()
        ll1l1l1l11l1l11lIl1l1.l1111ll1l111ll11Il1l1 = None

    def ll1l1llllll1l11lIl1l1(ll1l1l1l11l1l11lIl1l1) -> List[Type[l1l111111l111111Il1l1]]:
        return [l111l1ll1ll11lllIl1l1]

    def l1lllll1lll1111lIl1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        super().l1lllll1lll1111lIl1l1()
        sys.argv.append('--noreload')

    def l1lll1lll1111lllIl1l1(ll1l1l1l11l1l11lIl1l1, ll111ll1111llll1Il1l1: types.ModuleType) -> None:
        if (ll1l1l1l11l1l11lIl1l1.l1lll1lll1l1lll1Il1l1(ll111ll1111llll1Il1l1, 'django.core.management.commands.runserver')):
            ll1l1l1l11l1l11lIl1l1.ll1l1l1llll111llIl1l1()
            ll1l1l1l11l1l11lIl1l1.l1lll1l1l1l11lllIl1l1()

    def l1111l111lll111lIl1l1(ll1l1l1l11l1l11lIl1l1, ll11lll1ll1l1l11Il1l1: str) -> Optional["lllll111ll1l1111Il1l1"]:
        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        lll1ll1111l1ll11Il1l1 = l11111ll111111llIl1l1(ll11lll1ll1l1l11Il1l1=ll11lll1ll1l1l11Il1l1, lll1llll111l11llIl1l1=ll1l1l1l11l1l11lIl1l1)
        return lll1ll1111l1ll11Il1l1

    def ll1l1l1llll111llIl1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        import django.core.management.commands.runserver

        lll11ll1l11ll111Il1l1 = django.core.management.commands.runserver.Command.handle

        def l11lll1l1l1l1ll1Il1l1(*ll111l1ll1l1llllIl1l1: Any, **lll1lll11ll1l111Il1l1: Any) -> Any:
            with l111ll11ll11l1l1Il1l1():
                l11ll1ll1l1111l1Il1l1 = lll1lll11ll1l111Il1l1.get('addrport')
                if ( not l11ll1ll1l1111l1Il1l1):
                    l11ll1ll1l1111l1Il1l1 = django.core.management.commands.runserver.Command.default_port

                l11ll1ll1l1111l1Il1l1 = l11ll1ll1l1111l1Il1l1.split(':')[ - 1]
                l11ll1ll1l1111l1Il1l1 = int(l11ll1ll1l1111l1Il1l1)
                ll1l1l1l11l1l11lIl1l1.l1111ll1l111ll11Il1l1 = l11ll1ll1l1111l1Il1l1

            return lll11ll1l11ll111Il1l1(*ll111l1ll1l1llllIl1l1, **lll1lll11ll1l111Il1l1)

        l1l1l1l11lll1l1lIl1l1.ll11l1l1l111ll11Il1l1(django.core.management.commands.runserver.Command, 'handle', l11lll1l1l1l1ll1Il1l1)

    def l1lll1l1l1l11lllIl1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        import django.core.management.commands.runserver

        lll11ll1l11ll111Il1l1 = django.core.management.commands.runserver.Command.get_handler

        def l11lll1l1l1l1ll1Il1l1(*ll111l1ll1l1llllIl1l1: Any, **lll1lll11ll1l111Il1l1: Any) -> Any:
            with l111ll11ll11l1l1Il1l1():
                assert ll1l1l1l11l1l11lIl1l1.l1111ll1l111ll11Il1l1
                ll1l1l1l11l1l11lIl1l1.ll1lll111l11l1llIl1l1 = ll1l1l1l11l1l11lIl1l1.l11lll11l1111l1lIl1l1(ll1l1l1l11l1l11lIl1l1.l1111ll1l111ll11Il1l1)
                if (env.page_reload_on_start):
                    ll1l1l1l11l1l11lIl1l1.ll1lll111l11l1llIl1l1.l111ll1ll1l1lll1Il1l1(2.0)

            return lll11ll1l11ll111Il1l1(*ll111l1ll1l1llllIl1l1, **lll1lll11ll1l111Il1l1)

        l1l1l1l11lll1l1lIl1l1.ll11l1l1l111ll11Il1l1(django.core.management.commands.runserver.Command, 'get_handler', l11lll1l1l1l1ll1Il1l1)

    def l1111lll11l1111lIl1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        super().l1111lll11l1111lIl1l1()

        import django.core.handlers.base

        lll11ll1l11ll111Il1l1 = django.core.handlers.base.BaseHandler.get_response

        def l11lll1l1l1l1ll1Il1l1(l1ll1ll11lll11llIl1l1: Any, l1lll1ll1lll1lllIl1l1: Any) -> Any:
            ll1111llllllllllIl1l1 = lll11ll1l11ll111Il1l1(l1ll1ll11lll11llIl1l1, l1lll1ll1lll1lllIl1l1)

            if ( not ll1l1l1l11l1l11lIl1l1.ll1lll111l11l1llIl1l1):
                return ll1111llllllllllIl1l1

            ll1ll11ll111111lIl1l1 = ll1111llllllllllIl1l1.get('content-type')

            if (( not ll1ll11ll111111lIl1l1 or 'text/html' not in ll1ll11ll111111lIl1l1)):
                return ll1111llllllllllIl1l1

            ll1l11l1lll11lllIl1l1 = ll1111llllllllllIl1l1.content

            if (isinstance(ll1l11l1lll11lllIl1l1, bytes)):
                ll1l11l1lll11lllIl1l1 = ll1l11l1lll11lllIl1l1.decode('utf-8')

            l1l1lll11llll11lIl1l1 = ll1l1l1l11l1l11lIl1l1.ll1lll111l11l1llIl1l1.l1l11ll11l1ll111Il1l1(ll1l11l1lll11lllIl1l1)

            ll1111llllllllllIl1l1.content = l1l1lll11llll11lIl1l1.encode('utf-8')
            ll1111llllllllllIl1l1['content-length'] = str(len(ll1111llllllllllIl1l1.content)).encode('ascii')
            return ll1111llllllllllIl1l1

        django.core.handlers.base.BaseHandler.get_response = l11lll1l1l1l1ll1Il1l1  # type: ignore

    def l1111l11l1l11l1lIl1l1(ll1l1l1l11l1l11lIl1l1, lll1lll1l111llllIl1l1: Path) -> None:
        super().l1111l11l1l11l1lIl1l1(lll1lll1l111llllIl1l1)

        from django.apps.registry import Apps

        ll1l1l1l11l1l11lIl1l1.llll1l1l111llll1Il1l1 = Apps.register_model

        def ll1l1llll11111l1Il1l1(*ll111l1ll1l1llllIl1l1: Any, **l1111l1l1ll1l1llIl1l1: Any) -> Any:
            pass

        Apps.register_model = ll1l1llll11111l1Il1l1

    def lll1lll1ll111l11Il1l1(ll1l1l1l11l1l11lIl1l1, lll1lll1l111llllIl1l1: Path, lll1llllllll11l1Il1l1: List[lllll111ll11ll11Il1l1]) -> None:
        super().lll1lll1ll111l11Il1l1(lll1lll1l111llllIl1l1, lll1llllllll11l1Il1l1)

        if ( not ll1l1l1l11l1l11lIl1l1.llll1l1l111llll1Il1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = ll1l1l1l11l1l11lIl1l1.llll1l1l111llll1Il1l1
