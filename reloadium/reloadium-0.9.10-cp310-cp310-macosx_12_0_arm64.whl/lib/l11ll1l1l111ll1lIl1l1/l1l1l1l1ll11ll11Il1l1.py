from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import l1l1lll11lllll1lIl1l1, llll11111l111lllIl1l1, public, ll111ll1ll111lllIl1l1, l11lllll1ll1l11lIl1l1
from reloadium.corium.l1ll1l111l11l11lIl1l1 import lll1lll11l1l1lllIl1l1, l111ll11ll111111Il1l1
from reloadium.corium.llll11111l111lllIl1l1 import l11llllll1l1llllIl1l1, l111ll11ll11l1l1Il1l1
from reloadium.corium.llll11l11lll1l1lIl1l1 import ll1lll1l111lll1lIl1l1
from reloadium.corium.l1ll1ll11111l1llIl1l1 import l1ll1ll11111l1llIl1l1
from reloadium.corium.l1llll1l11l11l11Il1l1 import l1ll1llll11ll1l1Il1l1
from reloadium.corium.llll11lll1llllllIl1l1 import lllll111ll1l1111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__all__ = ['l11l11l1ll11llllIl1l1', 'l111ll11l1l11111Il1l1', 'llllll111lll111lIl1l1']


l1111lll11111ll1Il1l1 = l1ll1ll11111l1llIl1l1.ll111l1l1l1111llIl1l1(__name__)


class l11l11l1ll11llllIl1l1:
    @classmethod
    def l11l1111l1ll1l1lIl1l1(llll11ll11l1lll1Il1l1, ll1ll1l1l1l1l111Il1l1: List[lllll111ll1l1111Il1l1]) -> None:
        for l1l11l11llll1lllIl1l1 in ll1ll1l1l1l1l111Il1l1:
            l1l11l11llll1lllIl1l1.l11ll1ll1ll1l1llIl1l1()

    @classmethod
    def l1ll1l1ll1111l11Il1l1(ll1l1l1l11l1l11lIl1l1) -> Optional[FrameType]:
        l11111llll11ll11Il1l1: FrameType = sys._getframe(2)
        lll1ll1111l1ll11Il1l1 = next(l11lllll1ll1l11lIl1l1.l11111llll11ll11Il1l1.llll1l1lll11l1llIl1l1(l11111llll11ll11Il1l1))
        return lll1ll1111l1ll11Il1l1


class l111ll11l1l11111Il1l1(l11l11l1ll11llllIl1l1):
    @classmethod
    def l11111ll1l1l11llIl1l1(llll11ll11l1lll1Il1l1, ll111l1ll1l1llllIl1l1: List[Any], l1111l1l1ll1l1llIl1l1: Dict[str, Any], ll1ll1l1l1l1l111Il1l1: Optional[List[lllll111ll1l1111Il1l1]]) -> Any:  # type: ignore
        with l111ll11ll11l1l1Il1l1():
            assert ll1lll1l111lll1lIl1l1.lll1ll1ll1ll1l1lIl1l1.l11ll1l1l111ll1lIl1l1
            l11111llll11ll11Il1l1 = ll1lll1l111lll1lIl1l1.lll1ll1ll1ll1l1lIl1l1.l11ll1l1l111ll1lIl1l1.llll1llll1ll11llIl1l1.l1ll11l11l1lll1lIl1l1()
            l11111llll11ll11Il1l1.lll11l111ll1lll1Il1l1()

            l1111ll11l111ll1Il1l1 = ll1lll1l111lll1lIl1l1.lll1ll1ll1ll1l1lIl1l1.l11lll111l11ll1lIl1l1.l111l11l11ll1ll1Il1l1(l11111llll11ll11Il1l1.ll11ll11l1l1l1l1Il1l1, l11111llll11ll11Il1l1.l11l1l1ll111llllIl1l1.lll1lllll1llll11Il1l1())
            assert l1111ll11l111ll1Il1l1
            l1ll111111ll1ll1Il1l1 = llll11ll11l1lll1Il1l1.l1ll1l1ll1111l11Il1l1()

            if (ll1ll1l1l1l1l111Il1l1):
                llll11ll11l1lll1Il1l1.l11l1111l1ll1l1lIl1l1(ll1ll1l1l1l1l111Il1l1)


        lll1ll1111l1ll11Il1l1 = l1111ll11l111ll1Il1l1(*ll111l1ll1l1llllIl1l1, **l1111l1l1ll1l1llIl1l1);        l11111llll11ll11Il1l1.ll11ll11l1l11l1lIl1l1.additional_info.pydev_step_stop = l1ll111111ll1ll1Il1l1  # type: ignore

        return lll1ll1111l1ll11Il1l1

    @classmethod
    async def l11ll111lllll1l1Il1l1(llll11ll11l1lll1Il1l1, ll111l1ll1l1llllIl1l1: List[Any], l1111l1l1ll1l1llIl1l1: Dict[str, Any], ll1ll1l1l1l1l111Il1l1: Optional[List[lllll111ll1l1111Il1l1]]) -> Any:  # type: ignore
        with l111ll11ll11l1l1Il1l1():
            assert ll1lll1l111lll1lIl1l1.lll1ll1ll1ll1l1lIl1l1.l11ll1l1l111ll1lIl1l1
            l11111llll11ll11Il1l1 = ll1lll1l111lll1lIl1l1.lll1ll1ll1ll1l1lIl1l1.l11ll1l1l111ll1lIl1l1.llll1llll1ll11llIl1l1.l1ll11l11l1lll1lIl1l1()
            l11111llll11ll11Il1l1.lll11l111ll1lll1Il1l1()

            l1111ll11l111ll1Il1l1 = ll1lll1l111lll1lIl1l1.lll1ll1ll1ll1l1lIl1l1.l11lll111l11ll1lIl1l1.l111l11l11ll1ll1Il1l1(l11111llll11ll11Il1l1.ll11ll11l1l1l1l1Il1l1, l11111llll11ll11Il1l1.l11l1l1ll111llllIl1l1.lll1lllll1llll11Il1l1())
            assert l1111ll11l111ll1Il1l1
            l1ll111111ll1ll1Il1l1 = llll11ll11l1lll1Il1l1.l1ll1l1ll1111l11Il1l1()

            if (ll1ll1l1l1l1l111Il1l1):
                llll11ll11l1lll1Il1l1.l11l1111l1ll1l1lIl1l1(ll1ll1l1l1l1l111Il1l1)


        lll1ll1111l1ll11Il1l1 = await l1111ll11l111ll1Il1l1(*ll111l1ll1l1llllIl1l1, **l1111l1l1ll1l1llIl1l1);        l11111llll11ll11Il1l1.ll11ll11l1l11l1lIl1l1.additional_info.pydev_step_stop = l1ll111111ll1ll1Il1l1  # type: ignore

        return lll1ll1111l1ll11Il1l1


class llllll111lll111lIl1l1(l11l11l1ll11llllIl1l1):
    @classmethod
    def l11111ll1l1l11llIl1l1(llll11ll11l1lll1Il1l1) -> Optional[ModuleType]:  # type: ignore
        with l111ll11ll11l1l1Il1l1():
            assert ll1lll1l111lll1lIl1l1.lll1ll1ll1ll1l1lIl1l1.l11ll1l1l111ll1lIl1l1
            l11111llll11ll11Il1l1 = ll1lll1l111lll1lIl1l1.lll1ll1ll1ll1l1lIl1l1.l11ll1l1l111ll1lIl1l1.llll1llll1ll11llIl1l1.l1ll11l11l1lll1lIl1l1()

            llll111l111111l1Il1l1 = Path(l11111llll11ll11Il1l1.l111ll1ll1l1ll1lIl1l1.f_globals['__spec__'].origin).absolute()
            l1l1l1111l1l11llIl1l1 = l11111llll11ll11Il1l1.l111ll1ll1l1ll1lIl1l1.f_globals['__name__']
            l11111llll11ll11Il1l1.lll11l111ll1lll1Il1l1()
            lll1ll1ll1llll11Il1l1 = ll1lll1l111lll1lIl1l1.lll1ll1ll1ll1l1lIl1l1.ll111llll1ll1l11Il1l1.lll11l11l1l1l1l1Il1l1(llll111l111111l1Il1l1)

            if ( not lll1ll1ll1llll11Il1l1):
                l1111lll11111ll1Il1l1.l11l11llll1l11llIl1l1('Could not retrieve src.', lll111lll1111ll1Il1l1={'file': l1ll1llll11ll1l1Il1l1.lll1lll1l111llllIl1l1(llll111l111111l1Il1l1), 
'fullname': l1ll1llll11ll1l1Il1l1.l1l1l1111l1l11llIl1l1(l1l1l1111l1l11llIl1l1)})

            assert lll1ll1ll1llll11Il1l1

        try:
            lll1ll1ll1llll11Il1l1.l111l1111111ll11Il1l1()
            lll1ll1ll1llll11Il1l1.l1ll1llllll1lll1Il1l1(l11lll111llll1llIl1l1=False)
            lll1ll1ll1llll11Il1l1.lll1lllll1111lllIl1l1(l11lll111llll1llIl1l1=False)
        except l11llllll1l1llllIl1l1 as ll1l1lll1lll1ll1Il1l1:
            l11111llll11ll11Il1l1.ll11lllllllll111Il1l1(ll1l1lll1lll1ll1Il1l1)
            return None

        import importlib.util

        l11l11l1l11lll11Il1l1 = l11111llll11ll11Il1l1.l111ll1ll1l1ll1lIl1l1.f_locals['__spec__']
        ll111ll1111llll1Il1l1 = importlib.util.module_from_spec(l11l11l1l11lll11Il1l1)

        lll1ll1ll1llll11Il1l1.ll1ll1l1ll1l11llIl1l1(ll111ll1111llll1Il1l1)
        return ll111ll1111llll1Il1l1


l111ll11ll111111Il1l1.l1111llll111ll1lIl1l1(lll1lll11l1l1lllIl1l1.l1111ll11ll111l1Il1l1, l111ll11l1l11111Il1l1.l11111ll1l1l11llIl1l1)
l111ll11ll111111Il1l1.l1111llll111ll1lIl1l1(lll1lll11l1l1lllIl1l1.l1l1l1llll111111Il1l1, l111ll11l1l11111Il1l1.l11ll111lllll1l1Il1l1)
l111ll11ll111111Il1l1.l1111llll111ll1lIl1l1(lll1lll11l1l1lllIl1l1.l1l1l111ll11l1l1Il1l1, llllll111lll111lIl1l1.l11111ll1l1l11llIl1l1)
