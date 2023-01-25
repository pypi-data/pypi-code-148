import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.lib.l1111lll11l11111Il1l1.lll1llll111l11llIl1l1 import l1l111ll11ll111lIl1l1
from reloadium.lib import ll1l111111llll1lIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass
class l1111l11lll1llllIl1l1(l1l111ll11ll111lIl1l1):
    ll11lll1ll1l1l11Il1l1 = 'Multiprocessing'

    def __post_init__(ll1l1l1l11l1l11lIl1l1) -> None:
        super().__post_init__()

    def l1lll1lll1111lllIl1l1(ll1l1l1l11l1l11lIl1l1, ll111ll1111llll1Il1l1: types.ModuleType) -> None:
        if (ll1l1l1l11l1l11lIl1l1.l1lll1lll1l1lll1Il1l1(ll111ll1111llll1Il1l1, 'multiprocessing.popen_spawn_posix')):
            ll1l1l1l11l1l11lIl1l1.l111ll1l1l11l1llIl1l1(ll111ll1111llll1Il1l1)

        if (ll1l1l1l11l1l11lIl1l1.l1lll1lll1l1lll1Il1l1(ll111ll1111llll1Il1l1, 'multiprocessing.popen_spawn_win32')):
            ll1l1l1l11l1l11lIl1l1.l11111l11lll1111Il1l1(ll111ll1111llll1Il1l1)

    def l111ll1l1l11l1llIl1l1(ll1l1l1l11l1l11lIl1l1, ll111ll1111llll1Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = ll1l111111llll1lIl1l1.llll111l111ll1l1Il1l1.lllll1lll1l1l111Il1l1  # type: ignore

    def l11111l11lll1111Il1l1(ll1l1l1l11l1l11lIl1l1, ll111ll1111llll1Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = ll1l111111llll1lIl1l1.llll111l111ll1l1Il1l1.__init__  # type: ignore
