import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.l1l1l1l111l1ll1lIl1l1 import ll11lll1ll1lll1lIl1l1
from reloadium.lib.lll1l1111111lll1Il1l1.ll1lll111lll11llIl1l1 import ll111lll1ll11111Il1l1, l1ll1ll1ll1ll111Il1l1
from reloadium.corium.ll1ll111l1ll11llIl1l1 import l1l1llllll1l1lllIl1l1
from reloadium.corium.ll11ll11l1111l11Il1l1 import l1ll11ll11111l1lIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass(repr=False)
class llll1l1ll111ll11Il1l1(l1ll1ll1ll1ll111Il1l1):
    ll1lll111lll11llIl1l1: "l1lllll11lll11llIl1l1"
    l1ll1l1ll1ll1ll1Il1l1: List["Transaction"] = field(init=False, default_factory=list)

    def __post_init__(l1111l111ll1l1llIl1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().__post_init__()

        l11l11l111ll111lIl1l1 = list(_sessions.values())

        for ll1l11ll1l1l1l1lIl1l1 in l11l11l111ll111lIl1l1:
            if ( not ll1l11ll1l1l1l1lIl1l1.is_active):
                continue

            lll11lll111lll11Il1l1 = ll1l11ll1l1l1l1lIl1l1.begin_nested()
            l1111l111ll1l1llIl1l1.l1ll1l1ll1ll1ll1Il1l1.append(lll11lll111lll11Il1l1)

    def __repr__(l1111l111ll1l1llIl1l1) -> str:
        return 'DbMemento'

    def l1l1111l1llllll1Il1l1(l1111l111ll1l1llIl1l1) -> None:
        super().l1l1111l1llllll1Il1l1()

        while l1111l111ll1l1llIl1l1.l1ll1l1ll1ll1ll1Il1l1:
            lll11lll111lll11Il1l1 = l1111l111ll1l1llIl1l1.l1ll1l1ll1ll1ll1Il1l1.pop()
            if (lll11lll111lll11Il1l1.is_active):
                try:
                    lll11lll111lll11Il1l1.rollback()
                except :
                    pass

    def llllllll1ll1l1l1Il1l1(l1111l111ll1l1llIl1l1) -> None:
        super().llllllll1ll1l1l1Il1l1()

        while l1111l111ll1l1llIl1l1.l1ll1l1ll1ll1ll1Il1l1:
            lll11lll111lll11Il1l1 = l1111l111ll1l1llIl1l1.l1ll1l1ll1ll1ll1Il1l1.pop()
            if (lll11lll111lll11Il1l1.is_active):
                try:
                    lll11lll111lll11Il1l1.commit()
                except :
                    pass


@dataclass
class l1lllll11lll11llIl1l1(ll111lll1ll11111Il1l1):
    l11ll1llllll1ll1Il1l1 = 'Sqlalchemy'

    llll1lll1l111ll1Il1l1: List["Engine"] = field(init=False, default_factory=list)
    l11l11l111ll111lIl1l1: Set["Session"] = field(init=False, default_factory=set)
    llllllll1ll11111Il1l1: Tuple[int, ...] = field(init=False)

    def l1ll111lllllll1lIl1l1(l1111l111ll1l1llIl1l1, l111l11l11111111Il1l1: types.ModuleType) -> None:
        if (l1111l111ll1l1llIl1l1.lll1ll1l1lll1lllIl1l1(l111l11l11111111Il1l1, 'sqlalchemy')):
            l1111l111ll1l1llIl1l1.ll1l11lllll1l11lIl1l1(l111l11l11111111Il1l1)

        if (l1111l111ll1l1llIl1l1.lll1ll1l1lll1lllIl1l1(l111l11l11111111Il1l1, 'sqlalchemy.engine.base')):
            l1111l111ll1l1llIl1l1.ll111l1l1111l111Il1l1(l111l11l11111111Il1l1)

    def ll1l11lllll1l11lIl1l1(l1111l111ll1l1llIl1l1, l111l11l11111111Il1l1: Any) -> None:
        l1ll11l111lll111Il1l1 = Path(l111l11l11111111Il1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', l1ll11l111lll111Il1l1)[0]

        l1l1l1ll1l1111llIl1l1 = [int(llll1111l111l111Il1l1) for llll1111l111l111Il1l1 in __version__.split('.')]
        l1111l111ll1l1llIl1l1.llllllll1ll11111Il1l1 = tuple(l1l1l1ll1l1111llIl1l1)

    def lll1l1ll11l1l11lIl1l1(l1111l111ll1l1llIl1l1, l11ll1llllll1ll1Il1l1: str) -> Optional["l1l1llllll1l1lllIl1l1"]:
        l11111111llllll1Il1l1 = llll1l1ll111ll11Il1l1(l11ll1llllll1ll1Il1l1=l11ll1llllll1ll1Il1l1, ll1lll111lll11llIl1l1=l1111l111ll1l1llIl1l1)
        return l11111111llllll1Il1l1

    def ll111l1l1111l111Il1l1(l1111l111ll1l1llIl1l1, l111l11l11111111Il1l1: Any) -> None:
        llll1l11111l1111Il1l1 = locals().copy()

        llll1l11111l1111Il1l1.update({'original': l111l11l11111111Il1l1.Engine.__init__, 'reloader_code': ll11lll1ll1lll1lIl1l1, 'engines': l1111l111ll1l1llIl1l1.llll1lll1l111ll1Il1l1})





        lll1l11l1llllll1Il1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        l111111l1l1lll1lIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (l1111l111ll1l1llIl1l1.llllllll1ll11111Il1l1 <= (1, 3, 24, )):
            exec(lll1l11l1llllll1Il1l1, {**globals(), **llll1l11111l1111Il1l1}, llll1l11111l1111Il1l1)
        else:
            exec(l111111l1l1lll1lIl1l1, {**globals(), **llll1l11111l1111Il1l1}, llll1l11111l1111Il1l1)

        l1ll11ll11111l1lIl1l1.ll11lll11111l1llIl1l1(l111l11l11111111Il1l1.Engine, '__init__', llll1l11111l1111Il1l1['patched'])
