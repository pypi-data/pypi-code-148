from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.l1l1l1l111l1ll1lIl1l1 import ll11lll1ll1lll1lIl1l1
from reloadium.lib.lll1l1111111lll1Il1l1.ll1lll111lll11llIl1l1 import l1ll1ll1ll1ll111Il1l1
from reloadium.lib.lll1l1111111lll1Il1l1.ll11ll111l1111l1Il1l1 import ll11l1l11ll1lll1Il1l1
from reloadium.corium.l1l1llllllllllllIl1l1 import ll11111ll11l1ll1Il1l1, l1llll111l1ll11lIl1l1, ll1ll1ll1111l11lIl1l1, ll11l1l1111l11llIl1l1, ll1l1lll11l111l1Il1l1
from reloadium.corium.ll1ll111l1ll11llIl1l1 import l1l1llllll1l1lllIl1l1
from reloadium.corium.l1111llllll11111Il1l1 import l11l1111llll111lIl1l1
from reloadium.corium.ll11ll11l1111l11Il1l1 import l1ll11ll11111l1lIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from django.db import transaction
    from django.db.transaction import Atomic
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass(**ll1l1lll11l111l1Il1l1)
class ll1l111lll1l11llIl1l1(ll11l1l1111l11llIl1l1):
    l1111llll11l1111Il1l1 = 'Field'

    @classmethod
    def l1l1ll1l1ll1lll1Il1l1(ll1l11lll111111lIl1l1, l1ll1l11l11l11l1Il1l1: l11l1111llll111lIl1l1.llll1l111l1l11l1Il1l1, lll1l1ll1l1l1111Il1l1: Any, l11l11l111ll1lllIl1l1: l1llll111l1ll11lIl1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(lll1l1ll1l1l1111Il1l1, 'field') and isinstance(lll1l1ll1l1l1111Il1l1.field, Field))):
            return True

        return False

    def l11l1l1l111111llIl1l1(l1111l111ll1l1llIl1l1, ll1llll111l1lll1Il1l1: ll1ll1ll1111l11lIl1l1) -> bool:
        return True

    @classmethod
    def l11ll1l1l111l1llIl1l1(ll1l11lll111111lIl1l1) -> int:
        return 200


@dataclass(repr=False)
class llll1l1ll111ll11Il1l1(l1ll1ll1ll1ll111Il1l1):
    ll1111lllll1l1l1Il1l1: "Atomic" = field(init=False)

    l11lllllll1ll1l1Il1l1: bool = field(init=False, default=False)

    def __post_init__(l1111l111ll1l1llIl1l1) -> None:
        super().__post_init__()
        from django.db import transaction

        l1111l111ll1l1llIl1l1.ll1111lllll1l1l1Il1l1 = transaction.atomic()
        l1111l111ll1l1llIl1l1.ll1111lllll1l1l1Il1l1.__enter__()

    def l1l1111l1llllll1Il1l1(l1111l111ll1l1llIl1l1) -> None:
        super().l1l1111l1llllll1Il1l1()
        if (l1111l111ll1l1llIl1l1.l11lllllll1ll1l1Il1l1):
            return 

        l1111l111ll1l1llIl1l1.l11lllllll1ll1l1Il1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        l1111l111ll1l1llIl1l1.ll1111lllll1l1l1Il1l1.__exit__(None, None, None)

    def llllllll1ll1l1l1Il1l1(l1111l111ll1l1llIl1l1) -> None:
        super().llllllll1ll1l1l1Il1l1()

        if (l1111l111ll1l1llIl1l1.l11lllllll1ll1l1Il1l1):
            return 

        l1111l111ll1l1llIl1l1.l11lllllll1ll1l1Il1l1 = True
        l1111l111ll1l1llIl1l1.ll1111lllll1l1l1Il1l1.__exit__(None, None, None)

    def __repr__(l1111l111ll1l1llIl1l1) -> str:
        return 'DbMemento'


@dataclass
class l1ll1l111l1lllllIl1l1(ll11l1l11ll1lll1Il1l1):
    l11ll1llllll1ll1Il1l1 = 'Django'

    lll111l11l1ll1l1Il1l1: Optional[int] = field(init=False)
    ll1ll1l1l1ll111lIl1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    def __post_init__(l1111l111ll1l1llIl1l1) -> None:
        super().__post_init__()
        l1111l111ll1l1llIl1l1.lll111l11l1ll1l1Il1l1 = None

    def l11l1l111llllll1Il1l1(l1111l111ll1l1llIl1l1) -> List[Type[ll1ll1ll1111l11lIl1l1]]:
        return [ll1l111lll1l11llIl1l1]

    def ll1lll1l1l1l1l1lIl1l1(l1111l111ll1l1llIl1l1) -> None:
        super().ll1lll1l1l1l1l1lIl1l1()
        sys.argv.append('--noreload')

    def l1ll111lllllll1lIl1l1(l1111l111ll1l1llIl1l1, l111l11l11111111Il1l1: types.ModuleType) -> None:
        if (l1111l111ll1l1llIl1l1.lll1ll1l1lll1lllIl1l1(l111l11l11111111Il1l1, 'django.core.management.commands.runserver')):
            l1111l111ll1l1llIl1l1.lll111ll1l1llll1Il1l1()
            l1111l111ll1l1llIl1l1.llll11l11llllll1Il1l1()

    def lll1l1ll11l1l11lIl1l1(l1111l111ll1l1llIl1l1, l11ll1llllll1ll1Il1l1: str) -> Optional["l1l1llllll1l1lllIl1l1"]:
        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        l11111111llllll1Il1l1 = llll1l1ll111ll11Il1l1(l11ll1llllll1ll1Il1l1=l11ll1llllll1ll1Il1l1, ll1lll111lll11llIl1l1=l1111l111ll1l1llIl1l1)
        return l11111111llllll1Il1l1

    def lll111ll1l1llll1Il1l1(l1111l111ll1l1llIl1l1) -> None:
        import django.core.management.commands.runserver

        lll1l1l11lll11l1Il1l1 = django.core.management.commands.runserver.Command.handle

        def l111ll1lllll111lIl1l1(*l11l111ll1ll1l11Il1l1: Any, **l1l1111l11l1111lIl1l1: Any) -> Any:
            with ll11lll1ll1lll1lIl1l1():
                l1ll11lll1l1l1l1Il1l1 = l1l1111l11l1111lIl1l1.get('addrport')
                if ( not l1ll11lll1l1l1l1Il1l1):
                    l1ll11lll1l1l1l1Il1l1 = django.core.management.commands.runserver.Command.default_port

                l1ll11lll1l1l1l1Il1l1 = l1ll11lll1l1l1l1Il1l1.split(':')[ - 1]
                l1ll11lll1l1l1l1Il1l1 = int(l1ll11lll1l1l1l1Il1l1)
                l1111l111ll1l1llIl1l1.lll111l11l1ll1l1Il1l1 = l1ll11lll1l1l1l1Il1l1

            return lll1l1l11lll11l1Il1l1(*l11l111ll1ll1l11Il1l1, **l1l1111l11l1111lIl1l1)

        l1ll11ll11111l1lIl1l1.ll11lll11111l1llIl1l1(django.core.management.commands.runserver.Command, 'handle', l111ll1lllll111lIl1l1)

    def llll11l11llllll1Il1l1(l1111l111ll1l1llIl1l1) -> None:
        import django.core.management.commands.runserver

        lll1l1l11lll11l1Il1l1 = django.core.management.commands.runserver.Command.get_handler

        def l111ll1lllll111lIl1l1(*l11l111ll1ll1l11Il1l1: Any, **l1l1111l11l1111lIl1l1: Any) -> Any:
            with ll11lll1ll1lll1lIl1l1():
                assert l1111l111ll1l1llIl1l1.lll111l11l1ll1l1Il1l1
                l1111l111ll1l1llIl1l1.llll111l1ll1l111Il1l1 = l1111l111ll1l1llIl1l1.ll111l1lll11lll1Il1l1(l1111l111ll1l1llIl1l1.lll111l11l1ll1l1Il1l1)
                if (env.page_reload_on_start):
                    l1111l111ll1l1llIl1l1.llll111l1ll1l111Il1l1.l1llll111ll11lllIl1l1(2.0)

            return lll1l1l11lll11l1Il1l1(*l11l111ll1ll1l11Il1l1, **l1l1111l11l1111lIl1l1)

        l1ll11ll11111l1lIl1l1.ll11lll11111l1llIl1l1(django.core.management.commands.runserver.Command, 'get_handler', l111ll1lllll111lIl1l1)

    def l1l11l11l11111l1Il1l1(l1111l111ll1l1llIl1l1) -> None:
        super().l1l11l11l11111l1Il1l1()

        import django.core.handlers.base

        lll1l1l11lll11l1Il1l1 = django.core.handlers.base.BaseHandler.get_response

        def l111ll1lllll111lIl1l1(ll1111llll1l11l1Il1l1: Any, l1ll1ll11ll111llIl1l1: Any) -> Any:
            l11llllll11l1l11Il1l1 = lll1l1l11lll11l1Il1l1(ll1111llll1l11l1Il1l1, l1ll1ll11ll111llIl1l1)

            if ( not l1111l111ll1l1llIl1l1.llll111l1ll1l111Il1l1):
                return l11llllll11l1l11Il1l1

            lll1ll111ll11lllIl1l1 = l11llllll11l1l11Il1l1.get('content-type')

            if (( not lll1ll111ll11lllIl1l1 or 'text/html' not in lll1ll111ll11lllIl1l1)):
                return l11llllll11l1l11Il1l1

            l1ll11l111lll111Il1l1 = l11llllll11l1l11Il1l1.content

            if (isinstance(l1ll11l111lll111Il1l1, bytes)):
                l1ll11l111lll111Il1l1 = l1ll11l111lll111Il1l1.decode('utf-8')

            l11111lll1ll1lllIl1l1 = l1111l111ll1l1llIl1l1.llll111l1ll1l111Il1l1.l1111ll11ll1l11lIl1l1(l1ll11l111lll111Il1l1)

            l11llllll11l1l11Il1l1.content = l11111lll1ll1lllIl1l1.encode('utf-8')
            l11llllll11l1l11Il1l1['content-length'] = str(len(l11llllll11l1l11Il1l1.content)).encode('ascii')
            return l11llllll11l1l11Il1l1

        django.core.handlers.base.BaseHandler.get_response = l111ll1lllll111lIl1l1  # type: ignore

    def lll111111ll1ll1lIl1l1(l1111l111ll1l1llIl1l1, llll111111lll11lIl1l1: Path) -> None:
        super().lll111111ll1ll1lIl1l1(llll111111lll11lIl1l1)

        from django.apps.registry import Apps

        l1111l111ll1l1llIl1l1.ll1ll1l1l1ll111lIl1l1 = Apps.register_model

        def llll1llllll1l11lIl1l1(*l11l111ll1ll1l11Il1l1: Any, **llll11l1l11l1111Il1l1: Any) -> Any:
            pass

        Apps.register_model = llll1llllll1l11lIl1l1

    def ll1l1l1ll11l11l1Il1l1(l1111l111ll1l1llIl1l1, llll111111lll11lIl1l1: Path, l111lll1llllll1lIl1l1: List[ll11111ll11l1ll1Il1l1]) -> None:
        super().ll1l1l1ll11l11l1Il1l1(llll111111lll11lIl1l1, l111lll1llllll1lIl1l1)

        if ( not l1111l111ll1l1llIl1l1.ll1ll1l1l1ll111lIl1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = l1111l111ll1l1llIl1l1.ll1ll1l1l1ll111lIl1l1
