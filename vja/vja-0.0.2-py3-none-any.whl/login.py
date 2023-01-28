from configparser import NoOptionError, NoSectionError

import config
from apiclient import ApiClient

from vja import VjaError

api_client: ApiClient = None


def get_config():
    return config.get_parser()


def do_login(config=None) -> ApiClient:
    """Create and initialize (including authentication) an API client."""
    if not config:
        config = get_config()

    try:
        api_url = config.get("application", "api_url")
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
        api_client = do_login()
        return api_client
    except VjaError as e:
        print(e)
        exit(1)
