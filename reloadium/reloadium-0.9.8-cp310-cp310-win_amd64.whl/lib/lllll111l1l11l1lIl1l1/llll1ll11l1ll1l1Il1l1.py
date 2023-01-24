from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.l1lll1111l11ll1lIl1l1 import l1lll1l1ll1ll1llIl1l1
from reloadium.lib.lllll111l1l11l1lIl1l1.l11ll1l11111lll1Il1l1 import llllll11l111llllIl1l1
from reloadium.lib.lllll111l1l11l1lIl1l1.ll1ll11l11l1l11lIl1l1 import l111l11ll1l111llIl1l1
from reloadium.corium.l1lll1ll11ll1lllIl1l1 import l11ll1ll1lll11llIl1l1, lll1111l1l1l1l1lIl1l1, l1l1lll11ll1lll1Il1l1, l111l11l1l1l1l1lIl1l1, l1l1ll1l1lll11l1Il1l1
from reloadium.corium.l1111111l1lllll1Il1l1 import l1111111ll11l1llIl1l1
from reloadium.corium.llll1l1llll1llllIl1l1 import lllll1l11l11ll1lIl1l1
from reloadium.corium.l111ll1llll1llllIl1l1 import l1l1lllll111lll1Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from django.db import transaction
    from django.db.transaction import Atomic
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass(**l1l1ll1l1lll11l1Il1l1)
class lll1l1lll1l11111Il1l1(l111l11l1l1l1l1lIl1l1):
    l1ll1111111ll11lIl1l1 = 'Field'

    @classmethod
    def lll11111l11l111lIl1l1(lll11l1lll1llll1Il1l1, lll1l111l1l11lllIl1l1: lllll1l11l11ll1lIl1l1.l1lll1l1lllll11lIl1l1, l1l111l1l1l1lll1Il1l1: Any, l1llllll1l111l1lIl1l1: lll1111l1l1l1l1lIl1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(l1l111l1l1l1lll1Il1l1, 'field') and isinstance(l1l111l1l1l1lll1Il1l1.field, Field))):
            return True

        return False

    def l1l1l1ll11l111l1Il1l1(ll11l1llll1ll1l1Il1l1, l1ll1llll1111l11Il1l1: l1l1lll11ll1lll1Il1l1) -> bool:
        return True

    @classmethod
    def l11l1llll1ll1l11Il1l1(lll11l1lll1llll1Il1l1) -> int:
        return 200


@dataclass(repr=False)
class l1l11l1l11l1l1l1Il1l1(llllll11l111llllIl1l1):
    ll1111l1111111llIl1l1: "Atomic" = field(init=False)

    l1l1111l1lll1111Il1l1: bool = field(init=False, default=False)

    def __post_init__(ll11l1llll1ll1l1Il1l1) -> None:
        super().__post_init__()
        from django.db import transaction

        ll11l1llll1ll1l1Il1l1.ll1111l1111111llIl1l1 = transaction.atomic()
        ll11l1llll1ll1l1Il1l1.ll1111l1111111llIl1l1.__enter__()

    def l111l1l11lll1l1lIl1l1(ll11l1llll1ll1l1Il1l1) -> None:
        super().l111l1l11lll1l1lIl1l1()
        if (ll11l1llll1ll1l1Il1l1.l1l1111l1lll1111Il1l1):
            return 

        ll11l1llll1ll1l1Il1l1.l1l1111l1lll1111Il1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        ll11l1llll1ll1l1Il1l1.ll1111l1111111llIl1l1.__exit__(None, None, None)

    def l1111l111llll11lIl1l1(ll11l1llll1ll1l1Il1l1) -> None:
        super().l1111l111llll11lIl1l1()

        if (ll11l1llll1ll1l1Il1l1.l1l1111l1lll1111Il1l1):
            return 

        ll11l1llll1ll1l1Il1l1.l1l1111l1lll1111Il1l1 = True
        ll11l1llll1ll1l1Il1l1.ll1111l1111111llIl1l1.__exit__(None, None, None)

    def __repr__(ll11l1llll1ll1l1Il1l1) -> str:
        return 'DbMemento'


@dataclass
class llllll1l1lll11l1Il1l1(l111l11ll1l111llIl1l1):
    l11111l1l1ll1111Il1l1 = 'Django'

    ll11l11ll11lll11Il1l1: Optional[int] = field(init=False)
    l1ll1l1l1l1l11l1Il1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    def __post_init__(ll11l1llll1ll1l1Il1l1) -> None:
        super().__post_init__()
        ll11l1llll1ll1l1Il1l1.ll11l11ll11lll11Il1l1 = None

    def lllllll1l1l1111lIl1l1(ll11l1llll1ll1l1Il1l1) -> List[Type[l1l1lll11ll1lll1Il1l1]]:
        return [lll1l1lll1l11111Il1l1]

    @contextmanager
    def l11ll1lll11ll1l1Il1l1(ll11l1llll1ll1l1Il1l1, ll11l11111ll11llIl1l1: str, l1llll1ll11111llIl1l1: Dict[str, Any]) -> Generator[Tuple[str, Dict[str, Any]], None, None]:


        pass

    def ll11l11l11111111Il1l1(ll11l1llll1ll1l1Il1l1) -> None:
        super().ll11l11l11111111Il1l1()
        sys.argv.append('--noreload')

    def llll11llll1llll1Il1l1(ll11l1llll1ll1l1Il1l1, lll111lll11l1lllIl1l1: types.ModuleType) -> None:
        if (ll11l1llll1ll1l1Il1l1.l1l1ll111lll1ll1Il1l1(lll111lll11l1lllIl1l1, 'django.core.management.commands.runserver')):
            ll11l1llll1ll1l1Il1l1.llllll11ll1ll1llIl1l1()
            ll11l1llll1ll1l1Il1l1.llll11111l1l11l1Il1l1()

    def l11l1ll1ll1lll1lIl1l1(ll11l1llll1ll1l1Il1l1, l11111l1l1ll1111Il1l1: str) -> Optional["l1111111ll11l1llIl1l1"]:
        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        l1l1111l1ll1llllIl1l1 = l1l11l1l11l1l1l1Il1l1(l11111l1l1ll1111Il1l1=l11111l1l1ll1111Il1l1, l11ll1l11111lll1Il1l1=ll11l1llll1ll1l1Il1l1)
        return l1l1111l1ll1llllIl1l1

    def llllll11ll1ll1llIl1l1(ll11l1llll1ll1l1Il1l1) -> None:
        import django.core.management.commands.runserver

        l11lll11lll11111Il1l1 = django.core.management.commands.runserver.Command.handle

        def l11ll1111lll1111Il1l1(*l1llll1l1lll1lllIl1l1: Any, **l1l11ll11lll1111Il1l1: Any) -> Any:
            with l1lll1l1ll1ll1llIl1l1():
                l1111111111lllllIl1l1 = l1l11ll11lll1111Il1l1.get('addrport')
                if ( not l1111111111lllllIl1l1):
                    l1111111111lllllIl1l1 = django.core.management.commands.runserver.Command.default_port

                l1111111111lllllIl1l1 = l1111111111lllllIl1l1.split(':')[ - 1]
                l1111111111lllllIl1l1 = int(l1111111111lllllIl1l1)
                ll11l1llll1ll1l1Il1l1.ll11l11ll11lll11Il1l1 = l1111111111lllllIl1l1

            return l11lll11lll11111Il1l1(*l1llll1l1lll1lllIl1l1, **l1l11ll11lll1111Il1l1)

        l1l1lllll111lll1Il1l1.ll1111l11lll1l11Il1l1(django.core.management.commands.runserver.Command, 'handle', l11ll1111lll1111Il1l1)

    def llll11111l1l11l1Il1l1(ll11l1llll1ll1l1Il1l1) -> None:
        import django.core.management.commands.runserver

        l11lll11lll11111Il1l1 = django.core.management.commands.runserver.Command.get_handler

        def l11ll1111lll1111Il1l1(*l1llll1l1lll1lllIl1l1: Any, **l1l11ll11lll1111Il1l1: Any) -> Any:
            with l1lll1l1ll1ll1llIl1l1():
                assert ll11l1llll1ll1l1Il1l1.ll11l11ll11lll11Il1l1
                ll11l1llll1ll1l1Il1l1.l1l11l1ll111111lIl1l1 = ll11l1llll1ll1l1Il1l1.ll1111ll111l11llIl1l1(ll11l1llll1ll1l1Il1l1.ll11l11ll11lll11Il1l1)
                if (env.page_reload_on_start):
                    ll11l1llll1ll1l1Il1l1.l1l11l1ll111111lIl1l1.l111l1ll11ll1l11Il1l1(2.0)

            return l11lll11lll11111Il1l1(*l1llll1l1lll1lllIl1l1, **l1l11ll11lll1111Il1l1)

        l1l1lllll111lll1Il1l1.ll1111l11lll1l11Il1l1(django.core.management.commands.runserver.Command, 'get_handler', l11ll1111lll1111Il1l1)

    def l1ll1l11l1l1l11lIl1l1(ll11l1llll1ll1l1Il1l1) -> None:
        super().l1ll1l11l1l1l11lIl1l1()

        import django.core.handlers.base

        l11lll11lll11111Il1l1 = django.core.handlers.base.BaseHandler.get_response

        def l11ll1111lll1111Il1l1(llll11l111ll11llIl1l1: Any, l1ll11ll11lll1llIl1l1: Any) -> Any:
            l1lll11ll111lll1Il1l1 = l11lll11lll11111Il1l1(llll11l111ll11llIl1l1, l1ll11ll11lll1llIl1l1)

            if ( not ll11l1llll1ll1l1Il1l1.l1l11l1ll111111lIl1l1):
                return l1lll11ll111lll1Il1l1

            lll111111lll11llIl1l1 = l1lll11ll111lll1Il1l1.get('content-type')

            if (( not lll111111lll11llIl1l1 or 'text/html' not in lll111111lll11llIl1l1)):
                return l1lll11ll111lll1Il1l1

            l111l111111l1111Il1l1 = l1lll11ll111lll1Il1l1.content

            if (isinstance(l111l111111l1111Il1l1, bytes)):
                l111l111111l1111Il1l1 = l111l111111l1111Il1l1.decode('utf-8')

            l1ll1lll1ll11lllIl1l1 = ll11l1llll1ll1l1Il1l1.l1l11l1ll111111lIl1l1.lll1l1l11ll11l1lIl1l1(l111l111111l1111Il1l1)

            l1lll11ll111lll1Il1l1.content = l1ll1lll1ll11lllIl1l1.encode('utf-8')
            l1lll11ll111lll1Il1l1['content-length'] = str(len(l1lll11ll111lll1Il1l1.content)).encode('ascii')
            return l1lll11ll111lll1Il1l1

        django.core.handlers.base.BaseHandler.get_response = l11ll1111lll1111Il1l1  # type: ignore

    def llllll111lll1lllIl1l1(ll11l1llll1ll1l1Il1l1, llll1111l11llll1Il1l1: Path) -> None:
        super().llllll111lll1lllIl1l1(llll1111l11llll1Il1l1)

        from django.apps.registry import Apps

        ll11l1llll1ll1l1Il1l1.l1ll1l1l1l1l11l1Il1l1 = Apps.register_model

        def l11lll1l1l1lll1lIl1l1(*l1llll1l1lll1lllIl1l1: Any, **lll11lll1lll1l1lIl1l1: Any) -> Any:
            pass

        Apps.register_model = l11lll1l1l1lll1lIl1l1

    def l111ll1lll1l11l1Il1l1(ll11l1llll1ll1l1Il1l1, llll1111l11llll1Il1l1: Path, l11ll111llllllllIl1l1: List[l11ll1ll1lll11llIl1l1]) -> None:
        super().l111ll1lll1l11l1Il1l1(llll1111l11llll1Il1l1, l11ll111llllllllIl1l1)

        if ( not ll11l1llll1ll1l1Il1l1.l1ll1l1l1l1l11l1Il1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = ll11l1llll1ll1l1Il1l1.l1ll1l1l1l1l11l1Il1l1
