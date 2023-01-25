from shutil import get_terminal_size

import pytest

_term_width = get_terminal_size()[0]  # NOTE: 関数内で取得するとstdout内の仮想端末のサイズになる為


def pytest_addoption(parser):
    group = parser.getgroup("k4sima")
    group.addoption(
        "--k4sima-skip",
        action="store_true",
        help="pytest-k4sima を無効にする",
    )


@pytest.fixture(name="print_")
def pretty_print(request):
    """printの出力を見やすくする"""

    _pad = "-"

    def _print(*a, **k):
        print(f"\n{' '+request.node.name+' ':{_pad}^{_term_width}}")
        print(*a, **k)
        print(f"{'':{_pad}^{_term_width}}\n")

    yield _print


@pytest.fixture(autouse=True)
def printcap(request, capsys, print_):
    """printした出力を表示する"""

    yield

    if not request.config.getoption("--k4sima-skip"):
        with capsys.disabled():
            print_(capsys.readouterr().out)


"""
@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    pass
"""
