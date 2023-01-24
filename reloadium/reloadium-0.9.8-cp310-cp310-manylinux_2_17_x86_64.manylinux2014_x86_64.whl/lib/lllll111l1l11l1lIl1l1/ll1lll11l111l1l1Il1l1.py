import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.l1lll1111l11ll1lIl1l1 import l1lll1l1ll1ll1llIl1l1
from reloadium.lib.lllll111l1l11l1lIl1l1.l11ll1l11111lll1Il1l1 import ll1ll111l1lllll1Il1l1, llllll11l111llllIl1l1
from reloadium.corium.l1111111l1lllll1Il1l1 import l1111111ll11l1llIl1l1
from reloadium.corium.l111ll1llll1llllIl1l1 import l1l1lllll111lll1Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass(repr=False)
class l1l11l1l11l1l1l1Il1l1(llllll11l111llllIl1l1):
    l11ll1l11111lll1Il1l1: "llllll1ll1l111l1Il1l1"
    llll11l1l1l1l1llIl1l1: List["Transaction"] = field(init=False, default_factory=list)

    def __post_init__(ll11l1llll1ll1l1Il1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().__post_init__()

        ll1111l1ll11l1l1Il1l1 = list(_sessions.values())

        for ll1111ll1l1l11l1Il1l1 in ll1111l1ll11l1l1Il1l1:
            if ( not ll1111ll1l1l11l1Il1l1.is_active):
                continue

            l1ll111l1ll11ll1Il1l1 = ll1111ll1l1l11l1Il1l1.begin_nested()
            ll11l1llll1ll1l1Il1l1.llll11l1l1l1l1llIl1l1.append(l1ll111l1ll11ll1Il1l1)

    def __repr__(ll11l1llll1ll1l1Il1l1) -> str:
        return 'DbMemento'

    def l111l1l11lll1l1lIl1l1(ll11l1llll1ll1l1Il1l1) -> None:
        super().l111l1l11lll1l1lIl1l1()

        while ll11l1llll1ll1l1Il1l1.llll11l1l1l1l1llIl1l1:
            l1ll111l1ll11ll1Il1l1 = ll11l1llll1ll1l1Il1l1.llll11l1l1l1l1llIl1l1.pop()
            if (l1ll111l1ll11ll1Il1l1.is_active):
                try:
                    l1ll111l1ll11ll1Il1l1.rollback()
                except :
                    pass

    def l1111l111llll11lIl1l1(ll11l1llll1ll1l1Il1l1) -> None:
        super().l1111l111llll11lIl1l1()

        while ll11l1llll1ll1l1Il1l1.llll11l1l1l1l1llIl1l1:
            l1ll111l1ll11ll1Il1l1 = ll11l1llll1ll1l1Il1l1.llll11l1l1l1l1llIl1l1.pop()
            if (l1ll111l1ll11ll1Il1l1.is_active):
                try:
                    l1ll111l1ll11ll1Il1l1.commit()
                except :
                    pass


@dataclass
class llllll1ll1l111l1Il1l1(ll1ll111l1lllll1Il1l1):
    l11111l1l1ll1111Il1l1 = 'Sqlalchemy'

    ll111l1l1lllllllIl1l1: List["Engine"] = field(init=False, default_factory=list)
    ll1111l1ll11l1l1Il1l1: Set["Session"] = field(init=False, default_factory=set)
    l1l111l11l1l1ll1Il1l1: Tuple[int, ...] = field(init=False)

    @contextmanager
    def l11ll1lll11ll1l1Il1l1(ll11l1llll1ll1l1Il1l1, ll11l11111ll11llIl1l1: str, l1llll1ll11111llIl1l1: Dict[str, Any]) -> Generator[Tuple[str, Dict[str, Any]], None, None]:


        pass

    def llll11llll1llll1Il1l1(ll11l1llll1ll1l1Il1l1, lll111lll11l1lllIl1l1: types.ModuleType) -> None:
        if (ll11l1llll1ll1l1Il1l1.l1l1ll111lll1ll1Il1l1(lll111lll11l1lllIl1l1, 'sqlalchemy')):
            ll11l1llll1ll1l1Il1l1.l11lll11lllll11lIl1l1(lll111lll11l1lllIl1l1)

        if (ll11l1llll1ll1l1Il1l1.l1l1ll111lll1ll1Il1l1(lll111lll11l1lllIl1l1, 'sqlalchemy.engine.base')):
            ll11l1llll1ll1l1Il1l1.l11lll1ll1lll1llIl1l1(lll111lll11l1lllIl1l1)

    def l11lll11lllll11lIl1l1(ll11l1llll1ll1l1Il1l1, lll111lll11l1lllIl1l1: Any) -> None:
        l111l111111l1111Il1l1 = Path(lll111lll11l1lllIl1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', l111l111111l1111Il1l1)[0]

        l11ll111lll1lll1Il1l1 = [int(l11ll11lll111l11Il1l1) for l11ll11lll111l11Il1l1 in __version__.split('.')]
        ll11l1llll1ll1l1Il1l1.l1l111l11l1l1ll1Il1l1 = tuple(l11ll111lll1lll1Il1l1)

    def l11l1ll1ll1lll1lIl1l1(ll11l1llll1ll1l1Il1l1, l11111l1l1ll1111Il1l1: str) -> Optional["l1111111ll11l1llIl1l1"]:
        l1l1111l1ll1llllIl1l1 = l1l11l1l11l1l1l1Il1l1(l11111l1l1ll1111Il1l1=l11111l1l1ll1111Il1l1, l11ll1l11111lll1Il1l1=ll11l1llll1ll1l1Il1l1)
        return l1l1111l1ll1llllIl1l1

    def l11lll1ll1lll1llIl1l1(ll11l1llll1ll1l1Il1l1, lll111lll11l1lllIl1l1: Any) -> None:
        l1111l1ll1ll1lllIl1l1 = locals().copy()

        l1111l1ll1ll1lllIl1l1.update({'original': lll111lll11l1lllIl1l1.Engine.__init__, 'reloader_code': l1lll1l1ll1ll1llIl1l1, 'engines': ll11l1llll1ll1l1Il1l1.ll111l1l1lllllllIl1l1})





        l11lll1l1111llllIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        l1lll111l11l111lIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (ll11l1llll1ll1l1Il1l1.l1l111l11l1l1ll1Il1l1 <= (1, 3, 24, )):
            exec(l11lll1l1111llllIl1l1, {**globals(), **l1111l1ll1ll1lllIl1l1}, l1111l1ll1ll1lllIl1l1)
        else:
            exec(l1lll111l11l111lIl1l1, {**globals(), **l1111l1ll1ll1lllIl1l1}, l1111l1ll1ll1lllIl1l1)

        l1l1lllll111lll1Il1l1.ll1111l11lll1l11Il1l1(lll111lll11l1lllIl1l1.Engine, '__init__', l1111l1ll1ll1lllIl1l1['patched'])
