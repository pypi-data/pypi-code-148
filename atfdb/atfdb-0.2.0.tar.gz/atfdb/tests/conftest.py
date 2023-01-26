import pytest

from atfdb.atfdb import host_connect, host_disconnect

SERVER_ADDRESS = "localhost"
SERVER_PORT = 5000


"""
:param scope:
    The scope for which this fixture is shared; one of ``"function"``
    (default), ``"class"``, ``"module"``, ``"package"`` or ``"session"``.

    This parameter may also be a callable which receives ``(fixture_name, config)``
    as parameters, and must return a ``str`` with one of the values mentioned above.

    See :ref:`dynamic scope` in the docs for more information.
"""


@pytest.fixture(scope="session")
def socket_server():
    host_connect(SERVER_ADDRESS, SERVER_PORT)

    yield

    host_disconnect()
