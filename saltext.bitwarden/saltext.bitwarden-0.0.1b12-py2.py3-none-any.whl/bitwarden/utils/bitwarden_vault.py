# pylint: disable=too-many-lines
"""
Bitwarden Vault Management REST API util module
"""
import json
import logging
import re
import urllib.parse

import humps
import requests
import salt.utils.files
import salt.utils.http
import salt.utils.url
import saltext.bitwarden.utils.bitwarden_general as bitwarden_general
import validators

log = logging.getLogger(__name__)


# Prefix that is appended to all log entries
LOG_PREFIX = "bitwarden:"


def _get_headers():  # pylint: disable=C0116
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    return headers


def lock(opts=None):
    """
    Lock the Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    lock_url = f"{vault_api_url}/lock"
    lock_results = {}
    lock_ret = salt.utils.http.query(lock_url, method="POST", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in lock_ret:
        log.error(
            '%s API query failed for "lock", status code: %s, error %s',
            LOG_PREFIX,
            lock_ret["status"],
            lock_ret["error"],
        )
        return False
    else:
        lock_results = json.loads(lock_ret["body"])
        if lock_results.get("success"):
            return True

    return False


def unlock(opts=None):
    """
    Unlock the Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

        password: ``None``
            The master password for the Bitwarden vault.

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url", "password"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    unlock_url = f"{vault_api_url}/unlock"
    unlock_data = {"password": config["password"]}
    unlock_results = {}
    unlock_ret = salt.utils.http.query(
        unlock_url, method="POST", data=json.dumps(unlock_data), header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in unlock_ret:
        log.error(
            '%s API query failed for "unlock", status code: %s, error %s',
            LOG_PREFIX,
            unlock_ret["status"],
            unlock_ret["error"],
        )
        return False
    else:
        unlock_results = json.loads(unlock_ret["body"])
        if unlock_results.get("success"):
            return True

    return False


def get_item(opts=None, item_id=None):
    """
    Get item from Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    item_id
        The object's item_id (UUID)

    Returns a dictionary containing the item if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    if not validators.uuid(item_id):
        log.error('%s Value for "item_id" must be a UUID', LOG_PREFIX)
        return False
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    item_url = f"{vault_api_url}/object/item/{item_id}"
    item_results = {}
    item_ret = salt.utils.http.query(item_url, method="GET", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in item_ret:
        log.error(
            '%s API query failed for "get_item", status code: %s, error %s',
            LOG_PREFIX,
            item_ret["status"],
            item_ret["error"],
        )
        return False
    else:
        item_results = json.loads(item_ret["body"])
        if item_results.get("success"):
            return humps.decamelize(item_results["data"])

    return False


def list_items(
    opts=None,
    search=None,
    url=None,
    folder_id=None,
    collection_id=None,
    organization_id=None,
    trash=None,
):
    """
    List items from Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    search
        List all items that contain this search term (string)

    url
        List all items with this URL/URI value (string)

    folder_id
        List all items with this unique folder identifier (UUID)

    collection_id
        List all items with this unique collection identifier (UUID)

    organization_id
        List all items with this unique Organization identifier (UUID)

    trash
        List all items in the Trash (boolean)

    Returns a list of dicts if successful or ``False`` if unsuccessful.
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    params = {}
    if search is not None:
        if not isinstance(search, str):
            log.error('%s Value for "search" must be a string.', LOG_PREFIX)
            return False
        else:
            params["search"] = search
    if url is not None:
        if not validators.url(url):
            log.error('%s Supplied URL "%s" is malformed', LOG_PREFIX, url)
            return False
        else:
            params["url"] = url
    if folder_id is not None:
        if not validators.uuid(folder_id):
            log.error('%s Supplied folder_id "%s" is malformed', LOG_PREFIX, folder_id)
            return False
        else:
            params["folderid"] = folder_id
    if collection_id is not None:
        if not validators.uuid(collection_id):
            log.error('%s Supplied collection_id "%s" is malformed', LOG_PREFIX, collection_id)
            return False
        else:
            params["collectionid"] = collection_id
    if organization_id is not None:
        if not validators.uuid(organization_id):
            log.error('%s Supplied organization_id "%s" is malformed', LOG_PREFIX, organization_id)
            return False
        else:
            params["organizationid"] = organization_id
    if trash is not None:
        if not isinstance(trash, bool):
            log.error('%s Value for "trash" must be a boolean.', LOG_PREFIX)
            return False
        elif trash:
            params["trash"] = "true"
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    items_url = f"{vault_api_url}/list/object/items{params}"
    items_results = {}
    items_ret = salt.utils.http.query(items_url, method="GET", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in items_ret:
        log.error(
            '%s API query failed for "list_items", status code: %s, error %s',
            LOG_PREFIX,
            items_ret["status"],
            items_ret["error"],
        )
        return False
    else:
        items_results = json.loads(items_ret["body"])
        if items_results.get("success"):
            return humps.decamelize(items_results["data"]["data"])

    return False


def get_item_field(opts=None, item_id=None, field=None):
    """
    Get a field for an item from Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    item_id
        The object's item_id (UUID)

    field
        The field to retrieve. Must be one of "username", "password", "uri", "totp", "notes", or "exposed".

    Returns a string containing the password if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    if not validators.uuid(item_id):
        log.error('%s Value for "item_id" must be a UUID', LOG_PREFIX)
        return False
    valid_fields = ["username", "password", "uri", "totp", "notes", "exposed"]
    if field not in valid_fields:
        log.error('%s Value for "field" must be one of "%s"', LOG_PREFIX, '", "'.join(valid_fields))
        return False
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    field_url = f"{vault_api_url}/object/{field}/{item_id}"
    field_results = {}
    try:
        field_ret = requests.get(field_url, headers=headers)
        field_results = field_ret.json()
    except requests.exceptions.RequestException as e_req:
        log.error('%s API query failed for "get_%s", error %s', LOG_PREFIX, field, e_req)
        return False

    # Check if the field is unset
    if field_ret.status_code == 400:
        pattern = re.compile("No [A-Za-z]+ available for this [A-Za-z]+.")
        if field_results.get("success") is False and pattern.match(field_results.get("message")):
            log.debug('%s Field "%s" for item "%s" is not set', LOG_PREFIX, field, item_id)
            return None
        elif field_results.get("success") is False and field_results.get("message") == "Not found.":
            log.debug('%s Item "%s" not found', LOG_PREFIX, item_id)
            return False
        else:
            log.error(
                '%s API query failed for "get_%s", status code: %s, error %s',
                LOG_PREFIX,
                field,
                field_ret.status_code,
                field_ret.reason,
            )
            return False
    elif field_ret.status_code == 200 and field_results.get("success") is True:
        return field_results["data"]["data"]

    return False


def get_folder(opts=None, folder_id=None):  # pylint: disable=C0116
    """
    Get a folder from Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    folder_id
        The object's folder_id (UUID)

    Returns a dictionary containing the folder if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    if not validators.uuid(folder_id):
        log.error('%s Value for "folder_id" must be a UUID', LOG_PREFIX)
        return False
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    folder_url = f"{vault_api_url}/object/folder/{folder_id}"
    folder_results = {}
    folder_ret = salt.utils.http.query(folder_url, method="GET", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in folder_ret:
        log.error(
            '%s API query failed for "get_folder", status code: %s, error %s',
            LOG_PREFIX,
            folder_ret["status"],
            folder_ret["error"],
        )
        return False
    else:
        folder_results = json.loads(folder_ret["body"])
        if folder_results.get("success"):
            return humps.decamelize(folder_results["data"])

    return False


def list_folders(opts=None, search=None):  # pylint: disable=C0116
    """
    List folders from Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    search
        List all folders that contain this search term (string)

    Returns a list of dictionaries if successful or ``False`` if unsuccessful.
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    params = {}
    if search is not None:
        if not isinstance(search, str):
            log.error('%s Value for "search" must be a string.', LOG_PREFIX)
            return False
        else:
            params["search"] = search
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    folders_url = f"{vault_api_url}/list/object/folders{params}"
    folders_results = {}
    folders_ret = salt.utils.http.query(folders_url, method="GET", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in folders_ret:
        log.error(
            '%s API query failed for "list_folders", status code: %s, error %s',
            LOG_PREFIX,
            folders_ret["status"],
            folders_ret["error"],
        )
        return False
    else:
        folders_results = json.loads(folders_ret["body"])
        if folders_results.get("success"):
            return humps.decamelize(folders_results["data"]["data"])

    return False


def get_send(opts=None, send_id=None):  # pylint: disable=C0116
    """
    Get a send from Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    send_id
        The object's send_id (UUID)

    Returns a dictionary containing the send if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    if not validators.uuid(send_id):
        log.error('%s Value for "send_id" must be a UUID', LOG_PREFIX)
        return False
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    send_url = f"{vault_api_url}/object/send/{send_id}"
    send_results = {}
    send_ret = salt.utils.http.query(send_url, method="GET", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in send_ret:
        log.error(
            '%s API query failed for "get_send", status code: %s, error %s',
            LOG_PREFIX,
            send_ret["status"],
            send_ret["error"],
        )
        return False
    else:
        send_results = json.loads(send_ret["body"])
        if send_results.get("success"):
            return humps.decamelize(send_results["data"])

    return False


def list_sends(opts=None, search=None):  # pylint: disable=C0116
    """
    List sends from Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    search
        List all sends that contain this search term (string)

    Returns a list of dictionaries if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    params = {}
    if search is not None:
        if not isinstance(search, str):
            log.error('%s Value for "search" must be a string.', LOG_PREFIX)
            return False
        else:
            params["search"] = search
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    sends_url = f"{vault_api_url}/list/object/send{params}"
    sends_results = {}
    sends_ret = salt.utils.http.query(sends_url, method="GET", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in sends_ret:
        log.error(
            '%s API query failed for "list_sends", status code: %s, error %s',
            LOG_PREFIX,
            sends_ret["status"],
            sends_ret["error"],
        )
        return False
    else:
        sends_results = json.loads(sends_ret["body"])
        if sends_results.get("success"):
            return humps.decamelize(sends_results["data"]["data"])

    return False


def get_org_collection(
    opts=None, collection_id=None, organization_id=None
):  # pylint: disable=C0116
    """
    Get an organization collection

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    collection_id
        Unique identifier of the Collection (UUID)

    organization_id
        Unique identifier of the Organization (UUID)

    Returns a dictionary containing the organization collection if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    if not validators.uuid(collection_id):
        log.error('%s Value for "collection_id" must be a UUID', LOG_PREFIX)
        return False
    params = {}
    if not validators.uuid(organization_id):
        log.error('%s Value for "organization_id" must be a UUID', LOG_PREFIX)
        return False
    else:
        params["organizationid"] = organization_id
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    collection_url = f"{vault_api_url}/object/org-collection/{collection_id}{params}"
    collection_results = {}
    collection_ret = salt.utils.http.query(
        collection_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in collection_ret:
        log.error(
            '%s API query failed for "get_org_collection", status code: %s, error %s',
            LOG_PREFIX,
            collection_ret["status"],
            collection_ret["error"],
        )
        return False
    else:
        collection_results = json.loads(collection_ret["body"])
        if collection_results.get("success"):
            return humps.decamelize(collection_results["data"])

    return False


def list_org_collections(opts=None, organization_id=None, search=None):  # pylint: disable=C0116
    """
    List collections for an organization

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    organization_id
        Unique identifier of the Organization (UUID)

    search
        List all collections that contain this search term (string)

    Returns a list of dictionaries if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    params = {}
    if not validators.uuid(organization_id):
        log.error('%s Value for "organization_id" must be a UUID', LOG_PREFIX)
        return False
    else:
        params["organizationid"] = organization_id
    if search is not None:
        if not isinstance(search, str):
            log.error('%s Value for "search" must be a string.', LOG_PREFIX)
            return False
        else:
            params["search"] = search
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    collection_url = f"{vault_api_url}/list/object/org-collections{params}"
    collection_results = {}
    collection_ret = salt.utils.http.query(
        collection_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in collection_ret:
        log.error(
            '%s API query failed for "get_org_collection", status code: %s, error %s',
            LOG_PREFIX,
            collection_ret["status"],
            collection_ret["error"],
        )
        return False
    else:
        collection_results = json.loads(collection_ret["body"])
        if collection_results.get("success"):
            return humps.decamelize(collection_results["data"]["data"])

    return False


def list_collections(opts=None, search=None):  # pylint: disable=C0116
    """
    List Collections from all Organizations of which you are a member.
    Collections you do not have access to will not be listed.

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    search
        List all collections that contain this search term (string)

    Returns a list of dictionaries if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    params = {}
    if search is not None:
        if not isinstance(search, str):
            log.error('%s Value for "search" must be a string.', LOG_PREFIX)
            return False
        else:
            params["search"] = search
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    collection_url = f"{vault_api_url}/list/object/collections{params}"
    collection_results = {}
    collection_ret = salt.utils.http.query(
        collection_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in collection_ret:
        log.error(
            '%s API query failed for "get_org_collection", status code: %s, error %s',
            LOG_PREFIX,
            collection_ret["status"],
            collection_ret["error"],
        )
        return False
    else:
        collection_results = json.loads(collection_ret["body"])
        if collection_results.get("success"):
            return humps.decamelize(collection_results["data"]["data"])

    return False


def list_organizations(opts=None, search=None):  # pylint: disable=C0116
    """
    List organizations of which you are a member

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    search
        List only Organizations that contain this search term (string)

    Returns a list of dictionaries if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    params = {}
    if search is not None:
        if not isinstance(search, str):
            log.error('%s Value for "search" must be a string.', LOG_PREFIX)
            return False
        else:
            params["search"] = search
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    organizations_url = f"{vault_api_url}/list/object/organizations{params}"
    organizations_results = {}
    organizations_ret = salt.utils.http.query(
        organizations_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in organizations_ret:
        log.error(
            '%s API query failed for "list_organizations", status code: %s, error %s',
            LOG_PREFIX,
            organizations_ret["status"],
            organizations_ret["error"],
        )
        return False
    else:
        organizations_results = json.loads(organizations_ret["body"])
        if organizations_results.get("success"):
            return humps.decamelize(organizations_results["data"]["data"])

    return False


def list_org_members(opts=None, organization_id=None):  # pylint: disable=C0116
    """
    List members of an organization

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    organization_id
        Unique identifier of the Organization (UUID)

    Returns a list of dictionaries if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    params = {}
    if organization_id is not None:
        if not validators.uuid(organization_id):
            log.error('%s Supplied organization_id "%s" is malformed', LOG_PREFIX, organization_id)
            return False
        else:
            params["organizationid"] = organization_id
    else:
        log.error("%s Parameter organization_id is required", LOG_PREFIX)
        return False
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    members_url = f"{vault_api_url}/list/object/org-members{params}"
    members_results = {}
    members_ret = salt.utils.http.query(members_url, method="GET", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in members_ret:
        log.error(
            '%s API query failed for "list_org_members", status code: %s, error %s',
            LOG_PREFIX,
            members_ret["status"],
            members_ret["error"],
        )
        return False
    else:
        members_results = json.loads(members_ret["body"])
        if members_results.get("success"):
            return humps.decamelize(members_results["data"]["data"])

    return False


def sync(opts=None):
    """
    Sync Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    sync_url = f"{vault_api_url}/sync"
    sync_results = {}
    sync_ret = salt.utils.http.query(sync_url, method="POST", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in sync_ret:
        log.error(
            '%s API query failed for "sync", status code: %s, error %s',
            LOG_PREFIX,
            sync_ret["status"],
            sync_ret["error"],
        )
        return False
    else:
        sync_results = json.loads(sync_ret["body"])
        if sync_results.get("success"):
            return True

    return False


def get_status(opts=None):
    """
    Get status of Bitwarden vault (using the Vault Management REST API)

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    Returns a dictionary containing the vault status if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    status_url = f"{vault_api_url}/status"
    status_results = {}
    status_ret = salt.utils.http.query(status_url, method="GET", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in status_ret:
        log.error(
            '%s API query failed for "status", status code: %s, error %s',
            LOG_PREFIX,
            status_ret["status"],
            status_ret["error"],
        )
        return False
    else:
        status_results = json.loads(status_ret["body"])
        if status_results.get("success"):
            return humps.decamelize(status_results["data"]["template"])

    return False


def generate_password(
    opts=None, uppercase=None, lowercase=None, numeric=None, special=None, length=None
):
    """
    Generate a passphrase

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    uppercase
        Include uppercase characters in the password (boolean)

    lowercase
        Include lowercase characters in the password (boolean)

    numeric
        Include numbers in the password (boolean)

    special
        Include special characters in the password (boolean)

    length
        Number of characters in the password (integer >= 5)

    Returns a string containing the generated password if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    params = {}
    if uppercase is not None:
        if not isinstance(uppercase, bool):
            log.error('%s Value for "uppercase" must be a boolean.', LOG_PREFIX)
            return False
        elif uppercase:
            params["uppercase"] = "true"
    if lowercase is not None:
        if not isinstance(lowercase, bool):
            log.error('%s Value for "lowercase" must be a boolean.', LOG_PREFIX)
            return False
        elif lowercase:
            params["lowercase"] = "true"
    if numeric is not None:
        if not isinstance(numeric, bool):
            log.error('%s Value for "numeric" must be a boolean.', LOG_PREFIX)
            return False
        elif numeric:
            params["number"] = "true"
    if special is not None:
        if not isinstance(special, bool):
            log.error('%s Value for "special" must be a boolean.', LOG_PREFIX)
            return False
        elif special:
            params["special"] = "true"
    if length is not None:
        if not isinstance(length, int):
            log.error('%s Value for "length" must be an integer.', LOG_PREFIX)
            return False
        elif length:
            params["length"] = str(length)
        if length < 5:
            log.error("%s Password length must be at least 5 characters.", LOG_PREFIX)
            return False
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    generate_url = f"{vault_api_url}/generate{params}"
    generate_results = {}
    generate_ret = salt.utils.http.query(
        generate_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in generate_ret:
        log.error(
            '%s API query failed for "generate_password", status code: %s, error %s',
            LOG_PREFIX,
            generate_ret["status"],
            generate_ret["error"],
        )
        return False
    else:
        generate_results = json.loads(generate_ret["body"])
        if generate_results.get("success"):
            return generate_results["data"]["data"]

    return False


def generate_passphrase(
    opts=None, words=None, separator=None, capitalize=None, number=None
):  # pylint: disable=C0116
    """
    Generate a passphrase

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    words
        Number of words in the passphrase (integer >= 3)

    separator
        Separator character in the passphrase

    capitalize
        Title-case the passphrase (boolean)

    number
        Include numbers in the passphrase (boolean)

    Returns a string containing the generated passphrase if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    params = {"passphrase": "true"}
    if words is not None:
        if not isinstance(words, int):
            log.error('%s Value for "words" must be an integer.', LOG_PREFIX)
            return False
        else:
            params["words"] = str(words)
        if words < 3:
            log.error("%s Passphrase length must be at least 3 words.", LOG_PREFIX)
            return False
    if separator is not None:
        if not isinstance(separator, str):
            log.error('%s Value for "separator" must be a string.', LOG_PREFIX)
            return False
        else:
            params["separator"] = separator
        if len(separator) != 1:
            log.error("%s Separator must be a single character.", LOG_PREFIX)
            return False
    if capitalize is not None:
        if not isinstance(capitalize, bool):
            log.error('%s Value for "capitalize" must be a boolean.', LOG_PREFIX)
            return False
        elif capitalize:
            params["capitalize"] = "true"
    if number is not None:
        if not isinstance(number, bool):
            log.error('%s Value for "number" must be a boolean.', LOG_PREFIX)
            return False
        elif number:
            params["includeNumber"] = "true"
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    generate_url = f"{vault_api_url}/generate{params}"
    generate_results = {}
    generate_ret = salt.utils.http.query(
        generate_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in generate_ret:
        log.error(
            '%s API query failed for "generate_passphrase", status code: %s, error %s',
            LOG_PREFIX,
            generate_ret["status"],
            generate_ret["error"],
        )
        return False
    else:
        generate_results = json.loads(generate_ret["body"])
        if generate_results.get("success"):
            return generate_results["data"]["data"]

    return False


def get_template(opts=None, template_type=None):  # pylint: disable=C0116
    """
    Get a template

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    template_type
        Type of template to retrieve. (One of: "item", "item.field", "item.login.url", "item.card",
        item.identity", item.securenote, "folder", "collection", "item-collections", "org-collection")

    profile
        Profile to use (optional)

    Returns a dictionary containing the template if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    if template_type not in (
        "item",
        "item.field",
        "item.login.url",
        "item.card",
        "item.identity",
        "item.securenote",
        "folder",
        "collection",
        "item-collections",
        "org-collection",
    ):
        log.error(
            '%s Value for "template_type" must be one of:  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s.',
            LOG_PREFIX,
            "item",
            "item.field",
            "item.login.url",
            "item.card",
            "item.identity",
            "item.securenote",
            "folder",
            "collection",
            "item-collections",
            "org-collection",
        )
        return False
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    template_url = f"{vault_api_url}/object/template/{template_type}"
    template_results = {}
    template_ret = salt.utils.http.query(
        template_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in template_ret:
        log.error(
            '%s API query failed for "get_template", status code: %s, error %s',
            LOG_PREFIX,
            template_ret["status"],
            template_ret["error"],
        )
        return False
    else:
        template_results = json.loads(template_ret["body"])
        if template_results.get("success"):
            return humps.decamelize(template_results["data"]["template"])

    return False


def get_fingerprint(opts=None):  # pylint: disable=C0116
    """
    Display user fingerprint

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    Returns a string containing the fingerprint if successful or ``False`` if unsuccessful
    """
    config = bitwarden_general.validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    fingerprint_url = f"{vault_api_url}/object/fingerprint/me"
    fingerprint_results = {}
    fingerprint_ret = salt.utils.http.query(
        fingerprint_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in fingerprint_ret:
        log.error(
            '%s API query failed for "get_fingerprint", status code: %s, error %s',
            LOG_PREFIX,
            fingerprint_ret["status"],
            fingerprint_ret["error"],
        )
        return False
    else:
        fingerprint_results = json.loads(fingerprint_ret["body"])
        if fingerprint_results.get("success"):
            return humps.decamelize(fingerprint_results["data"]["data"])

    return False
