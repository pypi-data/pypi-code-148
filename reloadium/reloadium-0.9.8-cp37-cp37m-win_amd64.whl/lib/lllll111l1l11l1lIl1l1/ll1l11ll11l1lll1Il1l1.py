import sys

from reloadium.corium.l111ll1llll1llllIl1l1.lll1ll1l111ll1llIl1l1 import lllll1ll1lll1ll1Il1l1

lllll1ll1lll1ll1Il1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class ll11l1l1111ll1l1Il1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = ll11l1l1111ll1l1Il1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite
