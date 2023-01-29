from configparser import NoOptionError, NoSectionError

from vja import VjaError
from vja import config
from vja.apiclient import ApiClient

api_client: ApiClient = None


def _do_login() -> ApiClient:
    """Create and initialize (including authentication) an API client."""
    try:
        api_url = config.get_parser().get("application", "api_url")
    except (NoSectionError, NoOptionError):
        raise VjaError("Login url not specified in %s.Dying." % config.get_path())

    client = ApiClient(api_url=api_url)
    client.authenticate()
    return client


def get_client() -> ApiClient:
    global api_client
    if api_client:
        return api_client
    try:
        api_client = _do_login()
        return api_client
    except VjaError as e:
        print(e)
        exit(1)
