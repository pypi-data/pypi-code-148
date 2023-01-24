from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.lllll111l1l11l1lIl1l1.l11ll1l11111lll1Il1l1 import ll1ll111l1lllll1Il1l1
from reloadium.corium.l1lll1ll11ll1lllIl1l1 import l11ll1ll1lll11llIl1l1
from reloadium.corium.l111ll1llll1llllIl1l1 import l1l1lllll111lll1Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass
class l1lll1l11111ll11Il1l1(ll1ll111l1lllll1Il1l1):
    l11111l1l1ll1111Il1l1 = 'PyGame'

    llll1ll111111111Il1l1: bool = field(init=False, default=False)

    def llll11llll1llll1Il1l1(ll11l1llll1ll1l1Il1l1, l11l1lll11l1l1l1Il1l1: types.ModuleType) -> None:
        if (ll11l1llll1ll1l1Il1l1.l1l1ll111lll1ll1Il1l1(l11l1lll11l1l1l1Il1l1, 'pygame.base')):
            ll11l1llll1ll1l1Il1l1.l1l11l1llll1l11lIl1l1()

    def l1l11l1llll1l11lIl1l1(ll11l1llll1ll1l1Il1l1) -> None:
        import pygame.display

        ll11ll1l1111ll1lIl1l1 = pygame.display.update

        def l11ll1l1l1l111llIl1l1(*l1llll1l1lll1lllIl1l1: Any, **lll11lll1lll1l1lIl1l1: Any) -> None:
            if (ll11l1llll1ll1l1Il1l1.llll1ll111111111Il1l1):
                l1l1lllll111lll1Il1l1.l1l1ll111l1lllllIl1l1(0.1)
                return None
            else:
                return ll11ll1l1111ll1lIl1l1(*l1llll1l1lll1lllIl1l1, **lll11lll1lll1l1lIl1l1)

        pygame.display.update = l11ll1l1l1l111llIl1l1

    def llllll111lll1lllIl1l1(ll11l1llll1ll1l1Il1l1, llll1111l11llll1Il1l1: Path) -> None:
        ll11l1llll1ll1l1Il1l1.llll1ll111111111Il1l1 = True

    def l111ll1lll1l11l1Il1l1(ll11l1llll1ll1l1Il1l1, llll1111l11llll1Il1l1: Path, l11ll111llllllllIl1l1: List[l11ll1ll1lll11llIl1l1]) -> None:
        ll11l1llll1ll1l1Il1l1.llll1ll111111111Il1l1 = False

    def l1lll11111l111llIl1l1(ll11l1llll1ll1l1Il1l1, ll1ll1l111l1llllIl1l1: Exception) -> None:
        ll11l1llll1ll1l1Il1l1.llll1ll111111111Il1l1 = False
