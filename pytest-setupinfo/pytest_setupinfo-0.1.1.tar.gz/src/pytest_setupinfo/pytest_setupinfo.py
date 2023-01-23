import pytest
import platform


def pytest_addoption(parser):
    parser.addoption(
        "--setupinfo", action="store_true", default=False, help="Setup Info"
    )


def pytest_configure(config):
    print(">" + "pytest_configure:")


@pytest.fixture()
def setupinfo(request):
    """
    Displays following setup related information using this setup_info fixture 

    Setup Name: Displays setup information in network
    Setup type: Displays whether setup is 32-bit or 64-bit arch type
    OS Info   : Displays kernel specific information
    CPU Type  : Displays CPU specific information
    Python Ver: Displays Python version

    """
    chk_info = request.config.getoption("setupinfo")

    def _info():
        """
        _info() private function
        """
        print("\n" + "*" * 33)
        print("Setup Configuration details are:")
        print("*" * 33)
        print(f"Setup name: {platform.node()}")
        print(f"Setup type: {platform.machine()}")
        print(f"OS Info   : {platform.platform()}")
        print(f"CPU Type  : {platform.processor()}")
        print(f"Python Ver: {platform.python_version()}")

    if chk_info:
        _info()

def other_information(req_type=""):
    """
    This API return pytest specific information which requested by user

    Parameters
    ----------
    req_type: str
        user requst. options are version/plugin/fixture
        
    Returns
    -------
    it returns data based on user req_type value

        returns pytest.__version__ if req_type='version'
        rerurns avail_fixtures if req_type='fixtures'
        return  avail_plugins if req_type='plugins'
        
    Examples
    --------
    >>> other_information(req_type='version')
    >>> other_information(req_type='fixtures')
    >>> other_information(req_type='plugins')

    """

    avail_fixtures = ["sanity","release","regression"]
    avail_plugins = ["pytest-cov", "pytest-env", "pytest-nice"]

    if req_type == "version":
        return pytest.__version__

    if req_type == "fixtures":
        return avail_fixtures

    if req_type == "plugins":
        return avail_plugins
        
