"""
Bitwarden runner module

This module allows access to a Bitwarden vault.

:depends: pyhumps, requests, validators

This module requires the ``bw`` Bitwarden CLI utility to be installed.
Installation instructions are available
`here <https://bitwarden.com/help/cli/#download-and-install>`_.

This module primarily relies on the `Bitwarden Vault Management API
<https://bitwarden.com/help/vault-management-api/>`_ running locally on the master
using the ``bw serve`` feature of the Bitwarden CLI utility, as well as the
`Bitwarden Public (Organization Management) API
<https://bitwarden.com/help/api/>`_ for its functionality. A
small number of functions also rely on executing the ``bw`` client directly
(mostly for login/logout since those methods are not exposed through any other
API).

.. warning::
    The Bitwarden Vault Management API running on the master, once the vault is
    unlocked, has no authentication or other protection. All traffic is
    unencrypted. Any users who can access the HTTP server or observe traffic to
    it can gain access to the contents of the entire vault.

    Please ensure you take adequate measures to protect the HTTP server, such as
    ensuring it only binds to localhost, using firewall rules to limit access to
    the port to specific users (where possible), and limiting which users have
    access to any system on which it is running.

This module also requires a configuration profile to be configured in the master
configuration file.

Configuration example:

.. code-block:: yaml

    my-bitwarden-vault:
      driver: bitwarden
      cli_path: /bin/bw
      cli_conf_dir: /etc/salt/.bitwarden
      vault_url: https://bitwarden.com
      email: user@example.com
      password: CorrectHorseBatteryStaple
      vault_api_url: http://localhost:8087
      public_api_url: https://api.bitwarden.com
      client_id: user.25fa6fc6-deeb-4b42-a279-5e680b51aa58
      client_secret: AofieD0oexiex1mie3eigi9oojooF3
      org_client_id: organization.d0e19db4-38aa-4284-be3d-e80cff306e6c
      org_client_secret: aWMk2MBf4NWXfaevrKyxa3uqNXYVQy

The ``driver`` refers to the Bitwarden module, and must be set to ``bitwarden``
in order to use this module.

Other configuration options:

cli_path: ``None``
    The path to the bitwarden cli binary on the local system. If set to ``None``
    the module will use ``bw`` (Unix-like) or ``bw.exe`` (Windows) from the Salt
    user's ``PATH``.

cli_conf_dir: ``None``
    The path specifying a folder where the Bitwarden CLI will store configuration
    data.

vault_url: ``https://bitwarden.com``
    The URL for the Bitwarden vault.

email: ``None``
    The email address of the Bitwarden account to use.

password: ``None``
    The master password for the Bitwarden vault.

vault_api_url: ``http://localhost:8087``
    The URL for the Bitwarden Vault Management API.

public_api_url: ``https://api.bitwarden.com``
    The URL for the Bitwarden Bitwarden Public (Organization Management) API.

client_id: ``None``
    The OAUTH client_id

client_secret: ``None``
    The OAUTH client_secret

org_client_id: ``None``
    The OAUTH organizational client_id

org_client_secret: ``None``
    The OAUTH organizational client_secret

"""
import logging

import saltext.bitwarden.utils.bitwarden_cli as bitwarden_cli
import saltext.bitwarden.utils.bitwarden_vault as bitwarden_vault

log = logging.getLogger(__name__)

# Prefix that is appended to all log entries
LOG_PREFIX = "bitwarden:"

__virtualname__ = "bitwarden"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The bitwarden runner module is not implemented yet")
    return __virtualname__


def _get_config(profile=None):  # pylint: disable=C0116
    config = {}
    if profile:
        config = __salt__["config.get"](profile)
        if config.get("driver") != "bitwarden":
            log.error("The specified profile is not a bitwarden profile")
            return {}
    else:
        config = __salt__["config.get"]("bitwarden")
    if not config:
        log.debug("The config is not set")
        return {}

    return config


def login(profile=None):
    """
    Login to Bitwarden vault

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.login

    Returns ``True`` if successful or a dictionary containing an error if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_cli.login(opts=opts)


def logout(profile=None):
    """
    Logout of Bitwarden vault

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.logout

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_cli.logout(opts=opts)


def lock(profile=None):
    """
    Lock the Bitwarden vault

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.lock

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.lock(opts=opts)


def unlock(profile=None):
    """
    Unlock the Bitwarden vault

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.unlock

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.unlock(opts=opts)


def get_item(item_id=None, profile=None):
    """
    Get item from Bitwarden vault

    item_id
        The object's item_id (UUID)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_item item_id=2589f6cb-e6d1-4ba0-9f3a-e97f544d7ec4

    Returns a dict containing the item if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_item(opts=opts, item_id=item_id)


def list_items(
    profile=None,
    search=None,
    url=None,
    folder_id=None,
    collection_id=None,
    organization_id=None,
    trash=None,
):
    """
    List items from Bitwarden vault

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

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.list_items search="Example Item" url="https://host.example.com" \
        folder_id=762fdafd-7df2-42f3-bbe1-6e4ee614195b \
        collection_id=bc32045a-d3fc-43a6-8e6e-4cea88a71ad8 \
        organization_id=5262be67-d544-4a8a-b0f5-4032ebb0d1a3 trash=True

    Returns a list of dicts if successful or ``False`` if unsuccessful.
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.list_items(
        opts=opts,
        search=search,
        url=url,
        folder_id=folder_id,
        collection_id=collection_id,
        organization_id=organization_id,
        trash=trash,
    )


def get_username(item_id=None, profile=None):
    """
    Get username for an item from Bitwarden vault

    item_id
        The object's item_id (UUID)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_username item_id=2589f6cb-e6d1-4ba0-9f3a-e97f544d7ec4

    Returns a string containing the username if successful, ``None`` if the field is not set, or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_item_field(opts=opts, item_id=item_id, field="username")


def get_password(item_id=None, profile=None):
    """
    Get password for an item from Bitwarden vault

    item_id
        The object's item_id (UUID)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_password item_id=2589f6cb-e6d1-4ba0-9f3a-e97f544d7ec4

    Returns a string containing the password if successful, ``None`` if the field is not set, or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_item_field(opts=opts, item_id=item_id, field="password")


def get_uri(item_id=None, profile=None):
    """
    Get (first) URI for an item from Bitwarden vault

    item_id
        The object's item_id (UUID)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_uri item_id=2589f6cb-e6d1-4ba0-9f3a-e97f544d7ec4

    Returns a string containing the URI if successful, ``None`` if the field is not set, or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_item_field(opts=opts, item_id=item_id, field="uri")


def get_totp(item_id=None, profile=None):
    """
    Get TOTP for an item from Bitwarden vault

    item_id
        The object's item_id (UUID)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_totp item_id=2589f6cb-e6d1-4ba0-9f3a-e97f544d7ec4

    Returns a string containing the TOTP code if successful, ``None`` if the field is not set, or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_item_field(opts=opts, item_id=item_id, field="totp")


def get_notes(item_id=None, profile=None):
    """
    Get notes for an item from Bitwarden vault

    item_id
        The object's item_id (UUID)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_notes item_id=2589f6cb-e6d1-4ba0-9f3a-e97f544d7ec4

    Returns a string containing the notes if successful, ``None`` if the field is not set, or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_item_field(opts=opts, item_id=item_id, field="notes")


def get_exposed_password(item_id=None, profile=None):
    """
    Get a count of number of times a password has been exposed for an item from Bitwarden vault

    item_id
        The object's item_id (UUID)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_exposed_password item_id=2589f6cb-e6d1-4ba0-9f3a-e97f544d7ec4

    Returns a string containing the count if successful, ``None`` if the password field is not set, or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_item_field(opts=opts, item_id=item_id, field="exposed")


def get_folder(folder_id=None, profile=None):
    """
    Get a folder from Bitwarden vault

    folder_id
        The object's folder_id (UUID)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_folder folder_id=762fdafd-7df2-42f3-bbe1-6e4ee614195b

    Returns a dictionary containing the folder if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_folder(opts=opts, folder_id=folder_id)


def list_folders(search=None, profile=None):
    """
    List folders from Bitwarden vault

    search
        List all folders that contain this search term (string)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.list_folders search="Example Folder"

    Returns a list of dictionaries if successful or ``False`` if unsuccessful.
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.list_folders(opts=opts, search=search)


def get_send(send_id=None, profile=None):
    """
    Get a send from Bitwarden vault

    send_id
        The object's send_id (UUID)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_send send_id=762fdafd-7df2-42f3-bbe1-6e4ee614195b

    Returns a dictionary containing the send if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_send(opts=opts, send_id=send_id)


def list_sends(search=None, profile=None):
    """
    List sends from Bitwarden vault

    search
        List all sends that contain this search term (string)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.list_sends search="Example Send"

    Returns a list of dictionaries if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.list_sends(opts=opts, search=search)


def get_org_collection(collection_id=None, organization_id=None, profile=None):
    """
    Get an organization collection

    collection_id
        Unique identifier of the Collection (UUID)

    organization_id
        Unique identifier of the Organization (UUID)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_org_collection collection_id=bc32045a-d3fc-43a6-8e6e-4cea88a71ad8 \
        organization_id=5262be67-d544-4a8a-b0f5-4032ebb0d1a3

    Returns a dictionary containing the organization collection if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_org_collection(
        opts=opts, collection_id=collection_id, organization_id=organization_id
    )


def list_org_collections(organization_id=None, search=None, profile=None):
    """
    List collections for an organization

    organization_id
        Unique identifier of the Organization (UUID)

    search
        List all collections that contain this search term (string)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.list_org_collections organization_id=5262be67-d544-4a8a-b0f5-4032ebb0d1a3 search="Example Collection"

    Returns a list of dictionaries if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.list_org_collections(
        opts=opts, organization_id=organization_id, search=search
    )


def list_collections(search=None, profile=None):
    """
    List Collections from all Organizations of which you are a member.
    Collections you do not have access to will not be listed.

    search
        List all collections that contain this search term (string)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.list_collections search="Example Collection"

    Returns a list of dictionaries if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.list_collections(opts=opts, search=search)


def list_organizations(search=None, profile=None):
    """
    List organizations of which you are a member

    search
        List only Organizations that contain this search term (string)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.list_organizations search="Example Organization"

    Returns a list of dictionaries if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.list_organizations(opts=opts, search=search)


def list_org_members(organization_id=None, profile=None):
    """
    List members of an organization

    organization_id
        Unique identifier of the Organization (UUID)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.list_org_members organization_id=5262be67-d544-4a8a-b0f5-4032ebb0d1a3

    Returns a list of dictionaries if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.list_org_members(opts=opts, organization_id=organization_id)


def sync(profile=None):
    """
    Sync Bitwarden vault

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.sync

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.sync(opts=opts)


def get_status(use_cli=False, profile=None):
    """
    Get status of Bitwarden vault

    use_cli
        Use CLI to get status instead of REST API (boolean)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.status
    """
    opts = _get_config(profile=profile)

    if not isinstance(use_cli, bool):
        log.error('%s Value for "use_cli" must be a boolean.', LOG_PREFIX)
        return {"Error": 'Value for "use_cli" must be a boolean.'}

    if use_cli:
        status = bitwarden_cli.get_status(opts)
    else:
        status = bitwarden_vault.get_status(opts)

    return status


def generate_password(
    profile=None, uppercase=None, lowercase=None, numeric=None, special=None, length=None
):
    """
    Generate a passphrase

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

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.generate_password uppercase=True lowercase=True number=True special=True length=32
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.generate_password(
        opts=opts,
        uppercase=uppercase,
        lowercase=lowercase,
        numeric=numeric,
        special=special,
        length=length,
    )


def generate_passphrase(profile=None, words=None, separator=None, capitalize=None, number=None):
    """
    Generate a passphrase

    words
        Number of words in the passphrase (integer >= 3)

    separator
        Separator character in the passphrase

    capitalize
        Title-case the passphrase (boolean)

    number
        Include numbers in the passphrase (boolean)

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.generate_passphrase words=5 separator=":" capitalize=True number=True
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.generate_passphrase(
        opts=opts, words=words, separator=separator, capitalize=capitalize, number=number
    )


def get_template(profile=None, template_type=None):
    """
    Get a template

    template_type
        Type of template to retrieve. (One of: "item", "item.field", "item.login.url", "item.card",
        item.identity", item.securenote, "folder", "collection", "item-collections", "org-collection")

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_template template_type=item
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_template(opts=opts, template_type=template_type)


def get_fingerprint(profile=None):
    """
    Display user fingerprint

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt-run bitwarden.get_fingerprint
    """
    opts = _get_config(profile=profile)
    return bitwarden_vault.get_fingerprint(opts=opts)
