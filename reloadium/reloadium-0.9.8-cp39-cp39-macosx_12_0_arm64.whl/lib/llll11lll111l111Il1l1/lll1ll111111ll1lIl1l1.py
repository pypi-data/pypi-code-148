from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import l1lll11l1ll1ll11Il1l1, l1lll1111l11ll1lIl1l1, public, llll1llll1ll1ll1Il1l1, l111ll1llll1llllIl1l1
from reloadium.corium.lllll11l1ll111llIl1l1 import llll1lll11llllllIl1l1, l1111lll1ll1l111Il1l1
from reloadium.corium.l1lll1111l11ll1lIl1l1 import llll1l1l1llll111Il1l1, l1lll1l1ll1ll1llIl1l1
from reloadium.corium.l1l1lll1l111l11lIl1l1 import l1lll1ll111llll1Il1l1
from reloadium.corium.l1ll1ll1ll1lllllIl1l1 import l1ll1ll1ll1lllllIl1l1
from reloadium.corium.l11ll1ll11111ll1Il1l1 import l11l111ll1llll1lIl1l1
from reloadium.corium.l1111111l1lllll1Il1l1 import l1111111ll11l1llIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__all__ = ['lll11ll1l11ll1llIl1l1', 'l1lll1ll1111l111Il1l1', 'llllllll11lllll1Il1l1']


lll111llll1l1l11Il1l1 = l1ll1ll1ll1lllllIl1l1.l111l11l111l1l1lIl1l1(__name__)


class lll11ll1l11ll1llIl1l1:
    @classmethod
    def l111ll1111l1111lIl1l1(lll11l1lll1llll1Il1l1, l1l1lllll1ll1ll1Il1l1: List[l1111111ll11l1llIl1l1]) -> None:
        for l11l11l1llll1l1lIl1l1 in l1l1lllll1ll1ll1Il1l1:
            l11l11l1llll1l1lIl1l1.l111l1l11lll1l1lIl1l1()

    @classmethod
    def ll1l1l11ll1l1l11Il1l1(ll11l1llll1ll1l1Il1l1) -> Optional[FrameType]:
        l1lll111l111l111Il1l1: FrameType = sys._getframe(2)
        l1l1111l1ll1llllIl1l1 = next(l111ll1llll1llllIl1l1.l1lll111l111l111Il1l1.l1111llll1111111Il1l1(l1lll111l111l111Il1l1))
        return l1l1111l1ll1llllIl1l1


class l1lll1ll1111l111Il1l1(lll11ll1l11ll1llIl1l1):
    @classmethod
    def llllllllllllll11Il1l1(lll11l1lll1llll1Il1l1, l1llll1l1lll1lllIl1l1: List[Any], lll11lll1lll1l1lIl1l1: Dict[str, Any], l1l1lllll1ll1ll1Il1l1: Optional[List[l1111111ll11l1llIl1l1]]) -> Any:  # type: ignore
        with l1lll1l1ll1ll1llIl1l1():
            assert l1lll1ll111llll1Il1l1.l1l1ll11l1l111llIl1l1.llll11lll111l111Il1l1
            l1lll111l111l111Il1l1 = l1lll1ll111llll1Il1l1.l1l1ll11l1l111llIl1l1.llll11lll111l111Il1l1.l111lll1ll1ll1llIl1l1.lll1111ll1111l11Il1l1()
            l1lll111l111l111Il1l1.ll1l111ll1l111l1Il1l1()

            l111111l11lllll1Il1l1 = l1lll1ll111llll1Il1l1.l1l1ll11l1l111llIl1l1.lllll1111l11111lIl1l1.l1llll11l1ll1lllIl1l1(l1lll111l111l111Il1l1.l11l11l1ll1l1111Il1l1, l1lll111l111l111Il1l1.l1111ll11l11l111Il1l1.llll1l111lll1l11Il1l1())
            assert l111111l11lllll1Il1l1
            l1ll1l1l1l11l1llIl1l1 = lll11l1lll1llll1Il1l1.ll1l1l11ll1l1l11Il1l1()

            if (l1l1lllll1ll1ll1Il1l1):
                lll11l1lll1llll1Il1l1.l111ll1111l1111lIl1l1(l1l1lllll1ll1ll1Il1l1)


        l1l1111l1ll1llllIl1l1 = l111111l11lllll1Il1l1(*l1llll1l1lll1lllIl1l1, **lll11lll1lll1l1lIl1l1);        l1lll111l111l111Il1l1.l1l1llll1ll11l1lIl1l1.additional_info.pydev_step_stop = l1ll1l1l1l11l1llIl1l1  # type: ignore

        return l1l1111l1ll1llllIl1l1

    @classmethod
    async def l1111ll1lll111l1Il1l1(lll11l1lll1llll1Il1l1, l1llll1l1lll1lllIl1l1: List[Any], lll11lll1lll1l1lIl1l1: Dict[str, Any], l1l1lllll1ll1ll1Il1l1: Optional[List[l1111111ll11l1llIl1l1]]) -> Any:  # type: ignore
        with l1lll1l1ll1ll1llIl1l1():
            assert l1lll1ll111llll1Il1l1.l1l1ll11l1l111llIl1l1.llll11lll111l111Il1l1
            l1lll111l111l111Il1l1 = l1lll1ll111llll1Il1l1.l1l1ll11l1l111llIl1l1.llll11lll111l111Il1l1.l111lll1ll1ll1llIl1l1.lll1111ll1111l11Il1l1()
            l1lll111l111l111Il1l1.ll1l111ll1l111l1Il1l1()

            l111111l11lllll1Il1l1 = l1lll1ll111llll1Il1l1.l1l1ll11l1l111llIl1l1.lllll1111l11111lIl1l1.l1llll11l1ll1lllIl1l1(l1lll111l111l111Il1l1.l11l11l1ll1l1111Il1l1, l1lll111l111l111Il1l1.l1111ll11l11l111Il1l1.llll1l111lll1l11Il1l1())
            assert l111111l11lllll1Il1l1
            l1ll1l1l1l11l1llIl1l1 = lll11l1lll1llll1Il1l1.ll1l1l11ll1l1l11Il1l1()

            if (l1l1lllll1ll1ll1Il1l1):
                lll11l1lll1llll1Il1l1.l111ll1111l1111lIl1l1(l1l1lllll1ll1ll1Il1l1)


        l1l1111l1ll1llllIl1l1 = await l111111l11lllll1Il1l1(*l1llll1l1lll1lllIl1l1, **lll11lll1lll1l1lIl1l1);        l1lll111l111l111Il1l1.l1l1llll1ll11l1lIl1l1.additional_info.pydev_step_stop = l1ll1l1l1l11l1llIl1l1  # type: ignore

        return l1l1111l1ll1llllIl1l1


class llllllll11lllll1Il1l1(lll11ll1l11ll1llIl1l1):
    @classmethod
    def llllllllllllll11Il1l1(lll11l1lll1llll1Il1l1) -> Optional[ModuleType]:  # type: ignore
        with l1lll1l1ll1ll1llIl1l1():
            assert l1lll1ll111llll1Il1l1.l1l1ll11l1l111llIl1l1.llll11lll111l111Il1l1
            l1lll111l111l111Il1l1 = l1lll1ll111llll1Il1l1.l1l1ll11l1l111llIl1l1.llll11lll111l111Il1l1.l111lll1ll1ll1llIl1l1.lll1111ll1111l11Il1l1()

            ll1lll1ll11ll111Il1l1 = Path(l1lll111l111l111Il1l1.l1l111l1l1l1lll1Il1l1.f_globals['__spec__'].origin).absolute()
            l111l11llll11lllIl1l1 = l1lll111l111l111Il1l1.l1l111l1l1l1lll1Il1l1.f_globals['__name__']
            l1lll111l111l111Il1l1.ll1l111ll1l111l1Il1l1()
            ll11llllllll1lllIl1l1 = l1lll1ll111llll1Il1l1.l1l1ll11l1l111llIl1l1.l1l1llll11l1l111Il1l1.lll1ll1lll1l1l1lIl1l1(ll1lll1ll11ll111Il1l1)

            if ( not ll11llllllll1lllIl1l1):
                lll111llll1l1l11Il1l1.lll1l1l11ll1111lIl1l1('Could not retrieve src.', l1ll11ll1ll111llIl1l1={'file': l11l111ll1llll1lIl1l1.llll1111l11llll1Il1l1(ll1lll1ll11ll111Il1l1), 
'fullname': l11l111ll1llll1lIl1l1.l111l11llll11lllIl1l1(l111l11llll11lllIl1l1)})

            assert ll11llllllll1lllIl1l1

        try:
            ll11llllllll1lllIl1l1.l1ll11ll1l111l11Il1l1()
            ll11llllllll1lllIl1l1.l1lll11l1lll1l1lIl1l1(l1l11ll1l1l11111Il1l1=False)
            ll11llllllll1lllIl1l1.ll11l1l1l111ll11Il1l1(l1l11ll1l1l11111Il1l1=False)
        except llll1l1l1llll111Il1l1 as l1l1lll11llllll1Il1l1:
            l1lll111l111l111Il1l1.ll11l111lll11ll1Il1l1(l1l1lll11llllll1Il1l1)
            return None

        import importlib.util

        l1llll11l111ll11Il1l1 = l1lll111l111l111Il1l1.l1l111l1l1l1lll1Il1l1.f_locals['__spec__']
        lll111lll11l1lllIl1l1 = importlib.util.module_from_spec(l1llll11l111ll11Il1l1)

        ll11llllllll1lllIl1l1.l1l1ll1l1ll11l1lIl1l1(lll111lll11l1lllIl1l1)
        return lll111lll11l1lllIl1l1


l1111lll1ll1l111Il1l1.l111l1l1ll111lllIl1l1(llll1lll11llllllIl1l1.lll1lll1111l1l1lIl1l1, l1lll1ll1111l111Il1l1.llllllllllllll11Il1l1)
l1111lll1ll1l111Il1l1.l111l1l1ll111lllIl1l1(llll1lll11llllllIl1l1.lll11lll1l11111lIl1l1, l1lll1ll1111l111Il1l1.l1111ll1lll111l1Il1l1)
l1111lll1ll1l111Il1l1.l111l1l1ll111lllIl1l1(llll1lll11llllllIl1l1.l1ll11llll1l1lllIl1l1, llllllll11lllll1Il1l1.llllllllllllll11Il1l1)
