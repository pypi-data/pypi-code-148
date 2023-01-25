import sys

from reloadium.corium.ll11ll11l1111l11Il1l1.l11l11l1l1l1ll1lIl1l1 import l1lll11ll1l1lll1Il1l1

l1lll11ll1l1lll1Il1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class l1llllll1111llllIl1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = l1llllll1111llllIl1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite
