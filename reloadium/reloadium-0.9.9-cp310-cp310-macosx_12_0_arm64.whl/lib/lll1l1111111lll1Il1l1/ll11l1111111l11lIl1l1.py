import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.lib.lll1l1111111lll1Il1l1.ll1lll111lll11llIl1l1 import ll111lll1ll11111Il1l1
from reloadium.lib import l11l11l1lll1l1llIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass
class ll11111111ll1l1lIl1l1(ll111lll1ll11111Il1l1):
    l11ll1llllll1ll1Il1l1 = 'Multiprocessing'

    def __post_init__(l1111l111ll1l1llIl1l1) -> None:
        super().__post_init__()

    def l1ll111lllllll1lIl1l1(l1111l111ll1l1llIl1l1, l111l11l11111111Il1l1: types.ModuleType) -> None:
        if (l1111l111ll1l1llIl1l1.lll1ll1l1lll1lllIl1l1(l111l11l11111111Il1l1, 'multiprocessing.popen_spawn_posix')):
            l1111l111ll1l1llIl1l1.l1l1l111l1lll1l1Il1l1(l111l11l11111111Il1l1)

        if (l1111l111ll1l1llIl1l1.lll1ll1l1lll1lllIl1l1(l111l11l11111111Il1l1, 'multiprocessing.popen_spawn_win32')):
            l1111l111ll1l1llIl1l1.lll1111l1l11ll11Il1l1(l111l11l11111111Il1l1)

    def l1l1l111l1lll1l1Il1l1(l1111l111ll1l1llIl1l1, l111l11l11111111Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = l11l11l1lll1l1llIl1l1.ll11l1111111l11lIl1l1.ll1111ll111lll11Il1l1  # type: ignore

    def lll1111l1l11ll11Il1l1(l1111l111ll1l1llIl1l1, l111l11l11111111Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = l11l11l1lll1l1llIl1l1.ll11l1111111l11lIl1l1.__init__  # type: ignore
