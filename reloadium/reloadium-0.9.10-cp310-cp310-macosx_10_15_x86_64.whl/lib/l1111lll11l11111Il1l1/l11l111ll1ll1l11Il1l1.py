import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.llll11111l111lllIl1l1 import l111ll11ll11l1l1Il1l1
from reloadium.lib.l1111lll11l11111Il1l1.lll1llll111l11llIl1l1 import l1l111ll11ll111lIl1l1, lllll1l11lll1111Il1l1
from reloadium.corium.llll11lll1llllllIl1l1 import lllll111ll1l1111Il1l1
from reloadium.corium.l11lllll1ll1l11lIl1l1 import l1l1l1l11lll1l1lIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass(repr=False)
class l11111ll111111llIl1l1(lllll1l11lll1111Il1l1):
    lll1llll111l11llIl1l1: "l1l11l1l111l1l11Il1l1"
    ll1l11ll1l1l11l1Il1l1: List["Transaction"] = field(init=False, default_factory=list)

    def __post_init__(ll1l1l1l11l1l11lIl1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().__post_init__()

        l11l11ll1111l111Il1l1 = list(_sessions.values())

        for l11l1ll111l1l11lIl1l1 in l11l11ll1111l111Il1l1:
            if ( not l11l1ll111l1l11lIl1l1.is_active):
                continue

            llllll1lll11ll11Il1l1 = l11l1ll111l1l11lIl1l1.begin_nested()
            ll1l1l1l11l1l11lIl1l1.ll1l11ll1l1l11l1Il1l1.append(llllll1lll11ll11Il1l1)

    def __repr__(ll1l1l1l11l1l11lIl1l1) -> str:
        return 'DbMemento'

    def l11ll1ll1ll1l1llIl1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        super().l11ll1ll1ll1l1llIl1l1()

        while ll1l1l1l11l1l11lIl1l1.ll1l11ll1l1l11l1Il1l1:
            llllll1lll11ll11Il1l1 = ll1l1l1l11l1l11lIl1l1.ll1l11ll1l1l11l1Il1l1.pop()
            if (llllll1lll11ll11Il1l1.is_active):
                try:
                    llllll1lll11ll11Il1l1.rollback()
                except :
                    pass

    def l1l11111ll11ll11Il1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        super().l1l11111ll11ll11Il1l1()

        while ll1l1l1l11l1l11lIl1l1.ll1l11ll1l1l11l1Il1l1:
            llllll1lll11ll11Il1l1 = ll1l1l1l11l1l11lIl1l1.ll1l11ll1l1l11l1Il1l1.pop()
            if (llllll1lll11ll11Il1l1.is_active):
                try:
                    llllll1lll11ll11Il1l1.commit()
                except :
                    pass


@dataclass
class l1l11l1l111l1l11Il1l1(l1l111ll11ll111lIl1l1):
    ll11lll1ll1l1l11Il1l1 = 'Sqlalchemy'

    l1l1lll1111l1111Il1l1: List["Engine"] = field(init=False, default_factory=list)
    l11l11ll1111l111Il1l1: Set["Session"] = field(init=False, default_factory=set)
    ll1l1lll11llllllIl1l1: Tuple[int, ...] = field(init=False)

    def l1lll1lll1111lllIl1l1(ll1l1l1l11l1l11lIl1l1, ll111ll1111llll1Il1l1: types.ModuleType) -> None:
        if (ll1l1l1l11l1l11lIl1l1.l1lll1lll1l1lll1Il1l1(ll111ll1111llll1Il1l1, 'sqlalchemy')):
            ll1l1l1l11l1l11lIl1l1.llll1111111111l1Il1l1(ll111ll1111llll1Il1l1)

        if (ll1l1l1l11l1l11lIl1l1.l1lll1lll1l1lll1Il1l1(ll111ll1111llll1Il1l1, 'sqlalchemy.engine.base')):
            ll1l1l1l11l1l11lIl1l1.llll1l11l1llllllIl1l1(ll111ll1111llll1Il1l1)

    def llll1111111111l1Il1l1(ll1l1l1l11l1l11lIl1l1, ll111ll1111llll1Il1l1: Any) -> None:
        ll1l11l1lll11lllIl1l1 = Path(ll111ll1111llll1Il1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', ll1l11l1lll11lllIl1l1)[0]

        l11l11l111l1lll1Il1l1 = [int(l1lll1l1l11lll1lIl1l1) for l1lll1l1l11lll1lIl1l1 in __version__.split('.')]
        ll1l1l1l11l1l11lIl1l1.ll1l1lll11llllllIl1l1 = tuple(l11l11l111l1lll1Il1l1)

    def l1111l111lll111lIl1l1(ll1l1l1l11l1l11lIl1l1, ll11lll1ll1l1l11Il1l1: str) -> Optional["lllll111ll1l1111Il1l1"]:
        lll1ll1111l1ll11Il1l1 = l11111ll111111llIl1l1(ll11lll1ll1l1l11Il1l1=ll11lll1ll1l1l11Il1l1, lll1llll111l11llIl1l1=ll1l1l1l11l1l11lIl1l1)
        return lll1ll1111l1ll11Il1l1

    def llll1l11l1llllllIl1l1(ll1l1l1l11l1l11lIl1l1, ll111ll1111llll1Il1l1: Any) -> None:
        l111llll11l111llIl1l1 = locals().copy()

        l111llll11l111llIl1l1.update({'original': ll111ll1111llll1Il1l1.Engine.__init__, 'reloader_code': l111ll11ll11l1l1Il1l1, 'engines': ll1l1l1l11l1l11lIl1l1.l1l1lll1111l1111Il1l1})





        l11ll11111l1l111Il1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        l11111ll111lll11Il1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (ll1l1l1l11l1l11lIl1l1.ll1l1lll11llllllIl1l1 <= (1, 3, 24, )):
            exec(l11ll11111l1l111Il1l1, {**globals(), **l111llll11l111llIl1l1}, l111llll11l111llIl1l1)
        else:
            exec(l11111ll111lll11Il1l1, {**globals(), **l111llll11l111llIl1l1}, l111llll11l111llIl1l1)

        l1l1l1l11lll1l1lIl1l1.ll11l1l1l111ll11Il1l1(ll111ll1111llll1Il1l1.Engine, '__init__', l111llll11l111llIl1l1['patched'])
