import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.lib.lllll111l1l11l1lIl1l1.l11ll1l11111lll1Il1l1 import ll1ll111l1lllll1Il1l1
from reloadium.lib import llllllll11l11lllIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass
class l1ll1l111lll11l1Il1l1(ll1ll111l1lllll1Il1l1):
    l11111l1l1ll1111Il1l1 = 'Multiprocessing'

    def __post_init__(ll11l1llll1ll1l1Il1l1) -> None:
        super().__post_init__()

    def llll11llll1llll1Il1l1(ll11l1llll1ll1l1Il1l1, lll111lll11l1lllIl1l1: types.ModuleType) -> None:
        if (ll11l1llll1ll1l1Il1l1.l1l1ll111lll1ll1Il1l1(lll111lll11l1lllIl1l1, 'multiprocessing.popen_spawn_posix')):
            ll11l1llll1ll1l1Il1l1.llll11l1ll111l1lIl1l1(lll111lll11l1lllIl1l1)

        if (ll11l1llll1ll1l1Il1l1.l1l1ll111lll1ll1Il1l1(lll111lll11l1lllIl1l1, 'multiprocessing.popen_spawn_win32')):
            ll11l1llll1ll1l1Il1l1.ll1l111ll1l11l1lIl1l1(lll111lll11l1lllIl1l1)

    def llll11l1ll111l1lIl1l1(ll11l1llll1ll1l1Il1l1, lll111lll11l1lllIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = llllllll11l11lllIl1l1.l1l1l11l111l11l1Il1l1.lll111l1llll11l1Il1l1  # type: ignore

    def ll1l111ll1l11l1lIl1l1(ll11l1llll1ll1l1Il1l1, lll111lll11l1lllIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = llllllll11l11lllIl1l1.l1l1l11l111l11l1Il1l1.__init__  # type: ignore
