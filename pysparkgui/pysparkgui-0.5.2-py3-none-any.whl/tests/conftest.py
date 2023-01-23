# pytest configurations file


def pytest_sessionstart(session):
    print("START pysparkgui TESTS")
    from pysparkgui import _environment as env

    # True is default
    env.TESTING_MODE = True
    env.DEACTIVATE_ASYNC_CALLS = True
    env.TEST_BIVARIATE_PLOTS = True
