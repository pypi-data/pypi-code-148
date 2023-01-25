import sys

from reloadium.corium.l11lllll1ll1l11lIl1l1.ll111l111ll1l111Il1l1 import ll111l11llllllllIl1l1

ll111l11llllllllIl1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class l1l11l1l1ll111l1Il1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = l1l11l1l1ll111l1Il1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite
