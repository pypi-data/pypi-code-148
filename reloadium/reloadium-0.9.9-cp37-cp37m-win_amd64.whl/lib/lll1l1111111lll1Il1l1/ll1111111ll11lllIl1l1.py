from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.lll1l1111111lll1Il1l1.ll1lll111lll11llIl1l1 import ll111lll1ll11111Il1l1
from reloadium.corium.l1l1llllllllllllIl1l1 import ll11111ll11l1ll1Il1l1
from reloadium.corium.ll11ll11l1111l11Il1l1 import l1ll11ll11111l1lIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


@dataclass
class llll11111ll1ll11Il1l1(ll111lll1ll11111Il1l1):
    l11ll1llllll1ll1Il1l1 = 'PyGame'

    lll11l1l1lll1l11Il1l1: bool = field(init=False, default=False)

    def l1ll111lllllll1lIl1l1(l1111l111ll1l1llIl1l1, llll1ll1l1l11l1lIl1l1: types.ModuleType) -> None:
        if (l1111l111ll1l1llIl1l1.lll1ll1l1lll1lllIl1l1(llll1ll1l1l11l1lIl1l1, 'pygame.base')):
            l1111l111ll1l1llIl1l1.l11l11ll11ll11l1Il1l1()

    def l11l11ll11ll11l1Il1l1(l1111l111ll1l1llIl1l1) -> None:
        import pygame.display

        ll1llllll1111l1lIl1l1 = pygame.display.update

        def l1ll1l111ll1l1llIl1l1(*l11l111ll1ll1l11Il1l1: Any, **llll11l1l11l1111Il1l1: Any) -> None:
            if (l1111l111ll1l1llIl1l1.lll11l1l1lll1l11Il1l1):
                l1ll11ll11111l1lIl1l1.l1l1111l1ll11ll1Il1l1(0.1)
                return None
            else:
                return ll1llllll1111l1lIl1l1(*l11l111ll1ll1l11Il1l1, **llll11l1l11l1111Il1l1)

        pygame.display.update = l1ll1l111ll1l1llIl1l1

    def lll111111ll1ll1lIl1l1(l1111l111ll1l1llIl1l1, llll111111lll11lIl1l1: Path) -> None:
        l1111l111ll1l1llIl1l1.lll11l1l1lll1l11Il1l1 = True

    def ll1l1l1ll11l11l1Il1l1(l1111l111ll1l1llIl1l1, llll111111lll11lIl1l1: Path, l111lll1llllll1lIl1l1: List[ll11111ll11l1ll1Il1l1]) -> None:
        l1111l111ll1l1llIl1l1.lll11l1l1lll1l11Il1l1 = False

    def l1lllll1l11ll11lIl1l1(l1111l111ll1l1llIl1l1, ll11lll1llll1l11Il1l1: Exception) -> None:
        l1111l111ll1l1llIl1l1.lll11l1l1lll1l11Il1l1 = False
