"""
Bitwarden util module
"""
import logging
import os

import validators

log = logging.getLogger(__name__)

# Standard bitwarden cli client location
DEFAULT_CLI_PATH = "bw"
DEFAULT_CLI_CONF_DIR = "/etc/salt/.bitwarden"
DEFAULT_VAULT_API_URL = "http://localhost:8087"

# Prefix that is appended to all log entries
LOG_PREFIX = "bitwarden:"


def validate_opts(opts=None, opts_list=None):  # pylint: disable=C0116
    if isinstance(opts_list, list):
        for opt in opts_list:
            if opt == "cli_path":
                if not opts.get("cli_path") or not os.path.isfile(opts["cli_path"]):
                    opts["cli_path"] = DEFAULT_CLI_PATH
            elif opt == "cli_conf_dir":
                if not opts.get("cli_conf_dir"):
                    opts["cli_conf_dir"] = DEFAULT_CLI_CONF_DIR
            elif opt == "vault_url":
                if opts.get("vault_url"):
                    if not validators.url(opts["vault_url"]):
                        log.error(
                            '%s Supplied Bitwarden vault URL "%s" is malformed',
                            LOG_PREFIX,
                            opts.get("vault_url"),
                        )
                        return {
                            "Error": f'Supplied Bitwarden vault URL "{opts.get("vault_url")}" is malformed'
                        }
                else:
                    log.error("%s No Bitwarden vault URL specified", LOG_PREFIX)
                    return {"Error": "No Bitwarden vault URL specified"}
            elif opt == "email":
                if opts.get("email"):
                    if not validators.email(opts["email"]):
                        log.error(
                            '%s Value for email "%s" is not a valid email address',
                            LOG_PREFIX,
                            opts.get("email"),
                        )
                        return {
                            "Error": f'Value for email "{opts.get("email")}" is not a valid email address'
                        }
                else:
                    log.error("%s No email address supplied", LOG_PREFIX)
                    return {"Error": "No email address supplied"}
            elif opt == "password":
                if opts.get("password"):
                    if not isinstance(opts["password"], str):
                        log.error('%s Value for "password" must be a string', LOG_PREFIX)
                        return {"Error": 'Value for "password" must be a string'}
                else:
                    log.error("%s No password supplied", LOG_PREFIX)
                    return {"Error": "No password supplied"}
            elif opt == "vault_api_url":
                if opts.get("vault_api_url"):
                    if not validators.url(opts["vault_api_url"]):
                        log.error(
                            '%s Supplied Bitwarden CLI REST API URL "%s" is malformed',
                            LOG_PREFIX,
                            opts.get("vault_api_url"),
                        )
                        return {
                            "Error": f'Supplied Bitwarden CLI REST API URL "{opts.get("vault_api_url")}" is malformed'
                        }
                else:
                    log.error("%s No Bitwarden CLI REST API URL specified", LOG_PREFIX)
                    return {"Error": "No Bitwarden CLI REST API URL specified"}
            elif opt == "public_api_url":
                if opts.get("public_api_url"):
                    if not validators.url(opts["public_api_url"]):
                        log.error(
                            '%s Supplied Bitwarden Public API URL "%s" is malformed',
                            LOG_PREFIX,
                            opts.get("public_api_url"),
                        )
                        return {
                            "Error": f'Supplied Bitwarden Public API URL "{opts.get("public_api_url")}" is malformed'
                        }
                else:
                    log.error("%s No Bitwarden Public API URL specified", LOG_PREFIX)
                    return {"Error": "No Bitwarden Public API URL specified"}
            elif opt == "client_id":
                if opts.get("client_id"):
                    client_id_list = opts.get("client_id").split(".")
                    if client_id_list[0] != "user" or not validators.uuid(client_id_list[1]):
                        log.error(
                            '%s Supplied client_id "%s" is malformed',
                            LOG_PREFIX,
                            opts.get("client_id"),
                        )
                        return {
                            "Error": f'Supplied client_id "{opts.get("client_id")}" is malformed'
                        }
                else:
                    log.error("%s No client_id specified", LOG_PREFIX)
                    return {"Error": "No client_id specified"}
            elif opt == "client_secret":
                if opts.get("client_secret"):
                    if (
                        not isinstance(opts["client_secret"], str)
                        or len(opts["client_secret"]) != 30
                    ):
                        log.error(
                            '%s Value for "client_secret" must be a 30 character string',
                            LOG_PREFIX,
                        )
                        return {"Error": 'Value for "client_secret" must be a 30 character string'}
                else:
                    log.error("%s No client_secret supplied", LOG_PREFIX)
                    return {"Error": "No client_secret supplied"}
            elif opt == "org_client_id":
                if opts.get("org_client_id"):
                    org_client_id_list = opts.get("org_client_id").split(".")
                    if org_client_id_list[0] != "organization" or not validators.uuid(
                        org_client_id_list[1]
                    ):
                        log.error(
                            '%s Supplied org_client_id "%s" is malformed',
                            LOG_PREFIX,
                            opts.get("org_client_id"),
                        )
                        return {
                            "Error": f'Supplied org_client_id "{opts.get("org_client_id")}" is malformed'
                        }
                else:
                    log.error("%s No org_client_id specified", LOG_PREFIX)
                    return {"Error": "No org_client_id specified"}
            elif opt == "org_client_secret":
                if opts.get("org_client_secret"):
                    if (
                        not isinstance(opts["org_client_secret"], str)
                        or len(opts["org_client_secret"]) != 30
                    ):
                        log.error(
                            '%s Value for "org_client_secret" must be a 30 character string',
                            LOG_PREFIX,
                        )
                        return {
                            "Error": 'Value for "org_client_secret" must be a 30 character string'
                        }
                else:
                    log.error("%s No org_client_secret supplied", LOG_PREFIX)
                    return {"Error": "No org_client_secret supplied"}
            else:
                log.error("%s Invalid configuration option specified for validation", LOG_PREFIX)
                return {"Error": "Invalid configuration option specified for validation"}

        # Everything should be good, return configuration options
        return opts

    log.error("%s Invalid configuration option specified for validation", LOG_PREFIX)
    return {"Error": "Invalid configuration option specified for validation"}
