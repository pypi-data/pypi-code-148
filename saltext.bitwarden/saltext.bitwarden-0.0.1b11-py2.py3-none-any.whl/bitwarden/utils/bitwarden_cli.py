"""
Bitwarden CLI util module
"""
import json
import logging
import os
import subprocess

import humps
import saltext.bitwarden.utils.bitwarden_general as bitwarden_general

log = logging.getLogger(__name__)

# Standard bitwarden cli client location
DEFAULT_CLI_PATH = "bw"
DEFAULT_CLI_CONF_DIR = "/etc/salt/.bitwarden"
DEFAULT_VAULT_API_URL = "http://localhost:8087"

# Standard CLI arguments
cli_standard_args = [
    "--response",
    "--nointeraction",
]


# Prefix that is appended to all log entries
LOG_PREFIX = "bitwarden:"


def login(opts=None):
    """
    Login to Bitwarden vault

    opts
        Dictionary containing the following keys:

        cli_path: ``None``
            The path to the bitwarden cli binary on the local system. If set to ``None``
            the module will use ``bw`` (Unix-like) or ``bw.exe`` (Windows) from the Salt
            user's `PATH`.

        cli_conf_dir: ``None``
            The path specifying a folder where the Bitwarden CLI will store configuration
            data.

        vault_url: ``https://bitwarden.com``
            The URL for the Bitwarden vault.

        email: ``None``
            The email address of the Bitwarden account to use.

        client_id: ``None``
            The OAUTH client_id

        client_secret: ``None``
            The OAUTH client_secret

    Returns ``True`` if successful or a dictionary containing an error if unsuccessful
    """
    config = bitwarden_general.validate_opts(
        opts=opts, opts_list=["cli_path", "cli_conf_dir", "email", "client_id", "client_secret"]
    )
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}

    command = ["login", config["email"], "--apikey"]

    run = [config["cli_path"]] + command + cli_standard_args

    env = os.environ

    env["BW_CLIENTID"] = config["client_id"]
    env["BW_CLIENTSECRET"] = config["client_secret"]
    # Required due to https://github.com/bitwarden/cli/issues/381
    env["BITWARDENCLI_APPDATA_DIR"] = config["cli_conf_dir"]

    process = subprocess.Popen(run, env=env, stdout=subprocess.PIPE, universal_newlines=True)
    result = json.loads(process.communicate()[0])

    if result["success"]:
        log.debug(result["data"]["title"])
        return True
    elif "You are already logged in" in result["message"]:
        log.debug("%s %s", LOG_PREFIX, result["message"])
        return True
    else:
        log.error("%s %s", LOG_PREFIX, result["message"])
        return {"Error": humps.decamelize(result["message"])}

    return False


def logout(opts=None):
    """
    Logout of Bitwarden vault

    opts
        Dictionary containing the following keys:

        cli_path: ``None``
            The path to the bitwarden cli binary on the local system. If set to ``None``
            the module will use ``bw`` (Unix-like) or ``bw.exe`` (Windows) from the Salt
            user's ``PATH``.

        cli_conf_dir: ``None``
            The path specifying a folder where the Bitwarden CLI will store configuration
            data.

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["cli_path", "cli_conf_dir"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}

    command = [
        "logout",
    ]

    run = [config["cli_path"]] + command + cli_standard_args

    env = os.environ

    # Required due to https://github.com/bitwarden/cli/issues/381
    env["BITWARDENCLI_APPDATA_DIR"] = config["cli_conf_dir"]

    process = subprocess.Popen(run, env=env, stdout=subprocess.PIPE, universal_newlines=True)
    result = json.loads(process.communicate()[0])

    if result["success"]:
        log.debug(result["data"]["title"])
        return True
    elif "You are not logged in" in result["message"]:
        log.debug(result["message"])
        return True

    return False


def get_status(opts=None):
    """
    Get status of Bitwarden vault (using the `bw` CLI client)

    opts
        Dictionary containing the following keys:

        cli_path: ``None``
            The path to the bitwarden cli binary on the local system. If set to ``None``
            the module will use ``bw`` (Unix-like) or ``bw.exe`` (Windows) from the Salt
            user's `PATH`.

        cli_conf_dir: ``None``
            The path specifying a folder where the Bitwarden CLI will store configuration
            data.

    Returns a dictionary containing the vault status if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["cli_path", "cli_conf_dir"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}

    command = ["status"]

    run = [config["cli_path"]] + command + cli_standard_args

    env = os.environ

    # Required due to https://github.com/bitwarden/cli/issues/381
    env["BITWARDENCLI_APPDATA_DIR"] = config["cli_conf_dir"]

    process = subprocess.Popen(run, env=env, stdout=subprocess.PIPE, universal_newlines=True)
    result = json.loads(process.communicate()[0])

    if result["success"]:
        return humps.decamelize(result["data"]["template"])

    return False
