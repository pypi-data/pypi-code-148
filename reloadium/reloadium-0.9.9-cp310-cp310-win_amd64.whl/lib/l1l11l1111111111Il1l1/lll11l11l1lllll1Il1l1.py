from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import l1ll1l11ll11111lIl1l1, l1l1l1l111l1ll1lIl1l1, public, llllll11l111111lIl1l1, ll11ll11l1111l11Il1l1
from reloadium.corium.l11ll11111111l1lIl1l1 import l11l11ll1l1ll11lIl1l1, llll111llll1111lIl1l1
from reloadium.corium.l1l1l1l111l1ll1lIl1l1 import l111ll1ll11l1l11Il1l1, ll11lll1ll1lll1lIl1l1
from reloadium.corium.llllll1l1l1ll111Il1l1 import l1l1lll1l1lll11lIl1l1
from reloadium.corium.l11ll111l111llllIl1l1 import l11ll111l111llllIl1l1
from reloadium.corium.l11l11lll1l11111Il1l1 import llll111111l111llIl1l1
from reloadium.corium.ll1ll111l1ll11llIl1l1 import l1l1llllll1l1lllIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__all__ = ['l11l1llll1ll1l11Il1l1', 'll11lllll1ll1l1lIl1l1', 'l11l1l1ll1llllllIl1l1']


l1ll1lll1lll11llIl1l1 = l11ll111l111llllIl1l1.l1l1l11lll111lllIl1l1(__name__)


class l11l1llll1ll1l11Il1l1:
    @classmethod
    def ll1ll1llll1ll111Il1l1(ll1l11lll111111lIl1l1, ll1l1111l1l1lll1Il1l1: List[l1l1llllll1l1lllIl1l1]) -> None:
        for lll111111ll1lll1Il1l1 in ll1l1111l1l1lll1Il1l1:
            lll111111ll1lll1Il1l1.l1l1111l1llllll1Il1l1()

    @classmethod
    def l11ll111lllll1l1Il1l1(l1111l111ll1l1llIl1l1) -> Optional[FrameType]:
        lllll1l111l1l1l1Il1l1: FrameType = sys._getframe(2)
        l11111111llllll1Il1l1 = next(ll11ll11l1111l11Il1l1.lllll1l111l1l1l1Il1l1.lll1ll1ll1l1llllIl1l1(lllll1l111l1l1l1Il1l1))
        return l11111111llllll1Il1l1


class ll11lllll1ll1l1lIl1l1(l11l1llll1ll1l11Il1l1):
    @classmethod
    def l1l1ll111ll1111lIl1l1(ll1l11lll111111lIl1l1, l11l111ll1ll1l11Il1l1: List[Any], llll11l1l11l1111Il1l1: Dict[str, Any], ll1l1111l1l1lll1Il1l1: Optional[List[l1l1llllll1l1lllIl1l1]]) -> Any:  # type: ignore
        with ll11lll1ll1lll1lIl1l1():
            assert l1l1lll1l1lll11lIl1l1.ll1l11l1l1llllllIl1l1.l1l11l1111111111Il1l1
            lllll1l111l1l1l1Il1l1 = l1l1lll1l1lll11lIl1l1.ll1l11l1l1llllllIl1l1.l1l11l1111111111Il1l1.l11lll1l11ll1111Il1l1.lll1111lllll111lIl1l1()
            lllll1l111l1l1l1Il1l1.ll11ll1lll1l1111Il1l1()

            llll1ll1llll1ll1Il1l1 = l1l1lll1l1lll11lIl1l1.ll1l11l1l1llllllIl1l1.l1ll11l1l1l11lllIl1l1.l1111l1llll1lll1Il1l1(lllll1l111l1l1l1Il1l1.lll1l1l11l1l11l1Il1l1, lllll1l111l1l1l1Il1l1.ll11lll1l11111llIl1l1.ll111l11ll11ll1lIl1l1())
            assert llll1ll1llll1ll1Il1l1
            l1111ll1l1111111Il1l1 = ll1l11lll111111lIl1l1.l11ll111lllll1l1Il1l1()

            if (ll1l1111l1l1lll1Il1l1):
                ll1l11lll111111lIl1l1.ll1ll1llll1ll111Il1l1(ll1l1111l1l1lll1Il1l1)


        l11111111llllll1Il1l1 = llll1ll1llll1ll1Il1l1(*l11l111ll1ll1l11Il1l1, **llll11l1l11l1111Il1l1);        lllll1l111l1l1l1Il1l1.l1l1111l11l111l1Il1l1.additional_info.pydev_step_stop = l1111ll1l1111111Il1l1  # type: ignore

        return l11111111llllll1Il1l1

    @classmethod
    async def llll1l1ll1111lllIl1l1(ll1l11lll111111lIl1l1, l11l111ll1ll1l11Il1l1: List[Any], llll11l1l11l1111Il1l1: Dict[str, Any], ll1l1111l1l1lll1Il1l1: Optional[List[l1l1llllll1l1lllIl1l1]]) -> Any:  # type: ignore
        with ll11lll1ll1lll1lIl1l1():
            assert l1l1lll1l1lll11lIl1l1.ll1l11l1l1llllllIl1l1.l1l11l1111111111Il1l1
            lllll1l111l1l1l1Il1l1 = l1l1lll1l1lll11lIl1l1.ll1l11l1l1llllllIl1l1.l1l11l1111111111Il1l1.l11lll1l11ll1111Il1l1.lll1111lllll111lIl1l1()
            lllll1l111l1l1l1Il1l1.ll11ll1lll1l1111Il1l1()

            llll1ll1llll1ll1Il1l1 = l1l1lll1l1lll11lIl1l1.ll1l11l1l1llllllIl1l1.l1ll11l1l1l11lllIl1l1.l1111l1llll1lll1Il1l1(lllll1l111l1l1l1Il1l1.lll1l1l11l1l11l1Il1l1, lllll1l111l1l1l1Il1l1.ll11lll1l11111llIl1l1.ll111l11ll11ll1lIl1l1())
            assert llll1ll1llll1ll1Il1l1
            l1111ll1l1111111Il1l1 = ll1l11lll111111lIl1l1.l11ll111lllll1l1Il1l1()

            if (ll1l1111l1l1lll1Il1l1):
                ll1l11lll111111lIl1l1.ll1ll1llll1ll111Il1l1(ll1l1111l1l1lll1Il1l1)


        l11111111llllll1Il1l1 = await llll1ll1llll1ll1Il1l1(*l11l111ll1ll1l11Il1l1, **llll11l1l11l1111Il1l1);        lllll1l111l1l1l1Il1l1.l1l1111l11l111l1Il1l1.additional_info.pydev_step_stop = l1111ll1l1111111Il1l1  # type: ignore

        return l11111111llllll1Il1l1


class l11l1l1ll1llllllIl1l1(l11l1llll1ll1l11Il1l1):
    @classmethod
    def l1l1ll111ll1111lIl1l1(ll1l11lll111111lIl1l1) -> Optional[ModuleType]:  # type: ignore
        with ll11lll1ll1lll1lIl1l1():
            assert l1l1lll1l1lll11lIl1l1.ll1l11l1l1llllllIl1l1.l1l11l1111111111Il1l1
            lllll1l111l1l1l1Il1l1 = l1l1lll1l1lll11lIl1l1.ll1l11l1l1llllllIl1l1.l1l11l1111111111Il1l1.l11lll1l11ll1111Il1l1.lll1111lllll111lIl1l1()

            llll111l11ll11llIl1l1 = Path(lllll1l111l1l1l1Il1l1.lll1l1ll1l1l1111Il1l1.f_globals['__spec__'].origin).absolute()
            l1111lll1l1111l1Il1l1 = lllll1l111l1l1l1Il1l1.lll1l1ll1l1l1111Il1l1.f_globals['__name__']
            lllll1l111l1l1l1Il1l1.ll11ll1lll1l1111Il1l1()
            l11l1ll11ll11l11Il1l1 = l1l1lll1l1lll11lIl1l1.ll1l11l1l1llllllIl1l1.ll1111l11l11l1llIl1l1.l11ll11lll11ll1lIl1l1(llll111l11ll11llIl1l1)

            if ( not l11l1ll11ll11l11Il1l1):
                l1ll1lll1lll11llIl1l1.ll1lll111l1l1ll1Il1l1('Could not retrieve src.', l11l1lll1l11lll1Il1l1={'file': llll111111l111llIl1l1.llll111111lll11lIl1l1(llll111l11ll11llIl1l1), 
'fullname': llll111111l111llIl1l1.l1111lll1l1111l1Il1l1(l1111lll1l1111l1Il1l1)})

            assert l11l1ll11ll11l11Il1l1

        try:
            l11l1ll11ll11l11Il1l1.l11l11l1llll111lIl1l1()
            l11l1ll11ll11l11Il1l1.llll1l1lll11lll1Il1l1(l111l1l1lll11ll1Il1l1=False)
            l11l1ll11ll11l11Il1l1.lll111l1ll1lll1lIl1l1(l111l1l1lll11ll1Il1l1=False)
        except l111ll1ll11l1l11Il1l1 as ll1lllllll11l1llIl1l1:
            lllll1l111l1l1l1Il1l1.lll111lll1111l1lIl1l1(ll1lllllll11l1llIl1l1)
            return None

        import importlib.util

        l11ll1l1l1ll1111Il1l1 = lllll1l111l1l1l1Il1l1.lll1l1ll1l1l1111Il1l1.f_locals['__spec__']
        l111l11l11111111Il1l1 = importlib.util.module_from_spec(l11ll1l1l1ll1111Il1l1)

        l11l1ll11ll11l11Il1l1.ll1111l11llll1llIl1l1(l111l11l11111111Il1l1)
        return l111l11l11111111Il1l1


llll111llll1111lIl1l1.l11ll111ll1lllllIl1l1(l11l11ll1l1ll11lIl1l1.l1l1l1ll11ll1111Il1l1, ll11lllll1ll1l1lIl1l1.l1l1ll111ll1111lIl1l1)
llll111llll1111lIl1l1.l11ll111ll1lllllIl1l1(l11l11ll1l1ll11lIl1l1.l1111ll1l11llll1Il1l1, ll11lllll1ll1l1lIl1l1.llll1l1ll1111lllIl1l1)
llll111llll1111lIl1l1.l11ll111ll1lllllIl1l1(l11l11ll1l1ll11lIl1l1.l1ll1111lllll11lIl1l1, l11l1l1ll1llllllIl1l1.l1l1ll111ll1111lIl1l1)
