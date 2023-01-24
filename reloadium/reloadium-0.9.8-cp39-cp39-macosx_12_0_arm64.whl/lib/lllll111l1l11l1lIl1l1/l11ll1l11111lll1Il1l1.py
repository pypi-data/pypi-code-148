from abc import ABC
from contextlib import contextmanager
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.l1ll1ll1ll1lllllIl1l1 import lll1l111llll1lllIl1l1, l1ll1ll1ll1lllllIl1l1
from reloadium.corium.l1lll1ll11ll1lllIl1l1 import l11ll1ll1lll11llIl1l1, l1l1lll11ll1lll1Il1l1
from reloadium.corium.l1111111l1lllll1Il1l1 import l1111111ll11l1llIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from reloadium.lib.lllll111l1l11l1lIl1l1.ll1l1l1lll11llllIl1l1 import l11ll1l1111ll11lIl1l1
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass
class ll1ll111l1lllll1Il1l1:
    ll1l1l1lll11llllIl1l1: "l11ll1l1111ll11lIl1l1"

    l11111l1l1ll1111Il1l1: ClassVar[str] = NotImplemented
    l111ll111l1ll11lIl1l1: bool = field(init=False, default=False)

    l11l11llll1l1l1lIl1l1: lll1l111llll1lllIl1l1 = field(init=False)

    def __post_init__(ll11l1llll1ll1l1Il1l1) -> None:
        ll11l1llll1ll1l1Il1l1.l11l11llll1l1l1lIl1l1 = l1ll1ll1ll1lllllIl1l1.l111l11l111l1l1lIl1l1(ll11l1llll1ll1l1Il1l1.l11111l1l1ll1111Il1l1)
        ll11l1llll1ll1l1Il1l1.l11l11llll1l1l1lIl1l1.lll11lll11111lllIl1l1('Creating extension')
        ll11l1llll1ll1l1Il1l1.ll1l1l1lll11llllIl1l1.l1l1ll11l1l111llIl1l1.lll11l1ll1ll1l1lIl1l1.l1l111ll1ll1l11lIl1l1(ll11l1llll1ll1l1Il1l1.lllll1ll1111l11lIl1l1())

    def lllll1ll1111l11lIl1l1(ll11l1llll1ll1l1Il1l1) -> List[Type[l1l1lll11ll1lll1Il1l1]]:
        l1l1111l1ll1llllIl1l1 = []
        l1lll1ll11ll1lllIl1l1 = ll11l1llll1ll1l1Il1l1.lllllll1l1l1111lIl1l1()
        for l111l1l11l111111Il1l1 in l1lll1ll11ll1lllIl1l1:
            l111l1l11l111111Il1l1.ll11llll11l111llIl1l1 = ll11l1llll1ll1l1Il1l1.l11111l1l1ll1111Il1l1

        l1l1111l1ll1llllIl1l1.extend(l1lll1ll11ll1lllIl1l1)
        return l1l1111l1ll1llllIl1l1

    def llll1lllll1lll1lIl1l1(ll11l1llll1ll1l1Il1l1) -> None:
        ll11l1llll1ll1l1Il1l1.l111ll111l1ll11lIl1l1 = True

    def llll11llll1llll1Il1l1(ll11l1llll1ll1l1Il1l1, lll111lll11l1lllIl1l1: types.ModuleType) -> None:
        pass

    @contextmanager
    def l11ll1lll11ll1l1Il1l1(ll11l1llll1ll1l1Il1l1, ll11l11111ll11llIl1l1: str, l1llll1ll11111llIl1l1: Dict[str, Any]) -> Generator[Tuple[str, Dict[str, Any]], None, None]:


        yield (ll11l11111ll11llIl1l1, l1llll1ll11111llIl1l1, )

    def ll11l11l11111111Il1l1(ll11l1llll1ll1l1Il1l1) -> None:
        pass

    def l1lll11111l111llIl1l1(ll11l1llll1ll1l1Il1l1, ll1ll1l111l1llllIl1l1: Exception) -> None:
        pass

    def l11l1ll1ll1lll1lIl1l1(ll11l1llll1ll1l1Il1l1, l11111l1l1ll1111Il1l1: str) -> Optional[l1111111ll11l1llIl1l1]:
        return None

    def lll11lll111111l1Il1l1(ll11l1llll1ll1l1Il1l1, l11111l1l1ll1111Il1l1: str) -> Optional[l1111111ll11l1llIl1l1]:
        return None

    def lll11llll1ll1111Il1l1(ll11l1llll1ll1l1Il1l1, l11111l1l1ll1111Il1l1: str) -> Optional[l1111111ll11l1llIl1l1]:
        return None

    def lll1l1llll1l11l1Il1l1(ll11l1llll1ll1l1Il1l1, llll1111l11llll1Il1l1: Path) -> None:
        pass

    def llllll111lll1lllIl1l1(ll11l1llll1ll1l1Il1l1, llll1111l11llll1Il1l1: Path) -> None:
        pass

    def l111ll1lll1l11l1Il1l1(ll11l1llll1ll1l1Il1l1, llll1111l11llll1Il1l1: Path, l11ll111llllllllIl1l1: List[l11ll1ll1lll11llIl1l1]) -> None:
        pass

    def __eq__(ll11l1llll1ll1l1Il1l1, l1l11ll111ll1ll1Il1l1: Any) -> bool:
        return id(l1l11ll111ll1ll1Il1l1) == id(ll11l1llll1ll1l1Il1l1)

    def lllllll1l1l1111lIl1l1(ll11l1llll1ll1l1Il1l1) -> List[Type[l1l1lll11ll1lll1Il1l1]]:
        return []

    def l1l1ll111lll1ll1Il1l1(ll11l1llll1ll1l1Il1l1, lll111lll11l1lllIl1l1: types.ModuleType, l11111l1l1ll1111Il1l1: str) -> bool:
        l1l1111l1ll1llllIl1l1 = (hasattr(lll111lll11l1lllIl1l1, '__name__') and lll111lll11l1lllIl1l1.__name__ == l11111l1l1ll1111Il1l1)
        return l1l1111l1ll1llllIl1l1


@dataclass(repr=False)
class llllll11l111llllIl1l1(l1111111ll11l1llIl1l1):
    l11ll1l11111lll1Il1l1: ll1ll111l1lllll1Il1l1

    def __repr__(ll11l1llll1ll1l1Il1l1) -> str:
        return 'ExtensionMemento'
