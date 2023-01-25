from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.l1111lll11l11111Il1l1.lll1llll111l11llIl1l1 import l1l111ll11ll111lIl1l1
from reloadium.corium.lll11111lll1ll1lIl1l1 import lllll111ll11ll11Il1l1
from reloadium.corium.l11lllll1ll1l11lIl1l1 import l1l1l1l11lll1l1lIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass
class l1l11lll1lll1ll1Il1l1(l1l111ll11ll111lIl1l1):
    ll11lll1ll1l1l11Il1l1 = 'PyGame'

    ll11ll11l1ll1111Il1l1: bool = field(init=False, default=False)

    def l1lll1lll1111lllIl1l1(ll1l1l1l11l1l11lIl1l1, l111l111111l1111Il1l1: types.ModuleType) -> None:
        if (ll1l1l1l11l1l11lIl1l1.l1lll1lll1l1lll1Il1l1(l111l111111l1111Il1l1, 'pygame.base')):
            ll1l1l1l11l1l11lIl1l1.ll111111ll1l1lllIl1l1()

    def ll111111ll1l1lllIl1l1(ll1l1l1l11l1l11lIl1l1) -> None:
        import pygame.display

        ll1l11l111llll1lIl1l1 = pygame.display.update

        def ll11l1l1l1l11ll1Il1l1(*ll111l1ll1l1llllIl1l1: Any, **l1111l1l1ll1l1llIl1l1: Any) -> None:
            if (ll1l1l1l11l1l11lIl1l1.ll11ll11l1ll1111Il1l1):
                l1l1l1l11lll1l1lIl1l1.l1l111l11l11l11lIl1l1(0.1)
                return None
            else:
                return ll1l11l111llll1lIl1l1(*ll111l1ll1l1llllIl1l1, **l1111l1l1ll1l1llIl1l1)

        pygame.display.update = ll11l1l1l1l11ll1Il1l1

    def l1111l11l1l11l1lIl1l1(ll1l1l1l11l1l11lIl1l1, lll1lll1l111llllIl1l1: Path) -> None:
        ll1l1l1l11l1l11lIl1l1.ll11ll11l1ll1111Il1l1 = True

    def lll1lll1ll111l11Il1l1(ll1l1l1l11l1l11lIl1l1, lll1lll1l111llllIl1l1: Path, lll1llllllll11l1Il1l1: List[lllll111ll11ll11Il1l1]) -> None:
        ll1l1l1l11l1l11lIl1l1.ll11ll11l1ll1111Il1l1 = False

    def l111lll111l1lll1Il1l1(ll1l1l1l11l1l11lIl1l1, ll1l1l111l1ll111Il1l1: Exception) -> None:
        ll1l1l1l11l1l11lIl1l1.ll11ll11l1ll1111Il1l1 = False
