import os
from flask import Flask
from flask_basicauth import BasicAuth
from requests import get

__version__ = "0.1.0"


def _get_secret(
    name: str,
    default: str = "",
    getenv: bool = True,
    secrets_dir: str = "/var/run/secrets",
) -> str:
    """
    This function fetches a docker secret

    :param name: the name of the docker secret
    :param default: the default value if no secret found
    :param getenv: if environment variable should be fetched as fallback
    :param secrets_dir: the directory where the secrets are stored
    :returns: docker secret or environment variable depending on params
    """
    name_secret = name.lower()
    name_env = name.upper()

    # initialize value
    value = ""

    # try to read from secret file
    try:
        with open(
            os.path.join(secrets_dir, name_secret), "r", encoding="UTF-8"
        ) as secret_file:
            value = secret_file.read().strip()
    except IOError:
        # try to read from env if enabled
        if getenv:
            value = os.environ.get(name_env)

    # set default value if no value found
    if not value:
        value = default

    return value


app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = _get_secret("BASIC_AUTH_USERNAME")
app.config["BASIC_AUTH_PASSWORD"] = _get_secret("BASIC_AUTH_PASSWORD")
app.config["TELEGRAM_BOT_API_TOKEN"] = _get_secret("TELEGRAM_BOT_API_TOKEN")
basic_auth = BasicAuth(app)

from . import webhooks
