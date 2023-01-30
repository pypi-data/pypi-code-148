"""
Bitwarden sdb module

This module allows access to a Bitwarden vault using an ``sdb://`` URI

:depends: pyhumps, requests, validators

This module requires the ``bw`` Bitwarden CLI utility to be installed.
Installation instructions are available
`here <https://bitwarden.com/help/cli/#download-and-install>`_.

This module relies on the `Bitwarden Vault Management API
<https://bitwarden.com/help/vault-management-api/>`_ running locally on the
master or minion using the ``bw serve`` feature of the Bitwarden CLI utility
for its functionality.

.. warning::
    The Bitwarden Vault Management API running on the master or minion, once the
    vault is unlocked, has no authentication or other protection. All traffic is
    unencrypted. Any users who can access the HTTP server or observe traffic to
    it can gain access to the contents of the entire vault.

    Please ensure you take adequate measures to protect the HTTP server, such as
    ensuring it only binds to localhost, using firewall rules to limit access to
    the port to specific users (where possible), and limiting which users have
    access to any system on which it is running.

The Bitwarden vault must be logged in and unlocked in order for this module to
function. This can be done manually or via the execution, runner, or state
modules.

This module also requires a configuration profile to be configured in either the
minion or master configuration file.

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

This module permits access to items by UUID. Item UUIDs are immutable (don't
change) and unambiguous (will only ever refer to a single item).

The format of the SDB URI is as follows:

``sdb://<profile>/by-uuid/<uuid>/<object>``

Where ``<profile>`` is the profile defined in the master or minion configuration
file, ``<uuid>`` is the UUID of the item, and ``<object>`` is one of:

- name
- username
- password
- totp
- notes
- creation_date
- revision_date
- deleted_date
- password_revision_date

Additionally, password history can be retrieved with the following SDB URI
format:

``sdb://<profile>/by-uuid/<uuid>/password_history/by-index/<index>``

Where ``<profile>`` is the profile defined in the master or minion configuration
file, ``<uuid>`` is the UUID of the item, and ``index`` is a non-negative
integer specifying which password to retrieve from the history (0 being the
current password, 1 being the previous password, and so forth).

Lastly, custom fields can be retrieved with the following SDB URI format:

``sdb://<profile>/by-uuid/<uuid>/fields/by-name/<field_name>/<object>``

Where ``<profile>`` is the profile defined in the master or minion configuration
file, ``<uuid>`` is the UUID of the item, ``<field_name>`` is the name of
custom field, and object is one of:

- value
- type
- linked_id

Note that the custom field name must be unique within an item.
Bitwarden does not enforce unique custom field names, so that is left up to the
user.

The UUID of an item can be found using the Bitwarden CLI:

.. code-block:: bash

    bw list items --search "Google Account" --pretty
    [
      {
        "object": "item",
        "id": "2fa63ad5-e4e4-43d4-a089-3fadcf455be2",
        "organizationId": null,
        "folderId": null,
        "type": 1,
        "reprompt": 0,
        "name": "Google Account",
        "notes": null,
        "favorite": false,
        "fields": [
            {"name": "test_text", "value": "test", "type": 0, "linked_id": None},
            {"name": "test_hidden", "value": "test", "type": 1, "linked_id": None},
            {"name": "test_boolean", "value": "true", "type": 2, "linked_id": None},
            {"name": "test_linked_username", "value": None, "type": 3, "linked_id": 100},
            {"name": "test_linked_password", "value": None, "type": 3, "linked_id": 101},
        ],
        "login": {
          "uris": [
            {
              "match": null,
              "uri": "https://accounts.google.com"
            }
          ],
          "username": "user@example.com",
          "password": "aTjSsJvhQY5E24",
          "totp": "AEM1HEESIEV8YAED8THUBEHOOW",
          "passwordRevisionDate": null
        },
        "collectionIds": [],
        "revisionDate": "1970-01-01T00:00:00.000Z"
      }
    ]

To retrieve username for the above item, you would use:

.. code-block:: bash

    salt-run sdb.get 'sdb://my-bitwarden-vault/by-uuid/2fa63ad5-e4e4-43d4-a089-3fadcf455be2/username'

Similarly, for the password, use:

.. code-block:: bash

    salt-run sdb.get 'sdb://my-bitwarden-vault/by-uuid/2fa63ad5-e4e4-43d4-a089-3fadcf455be2/password'

To retrieve a custom field value, use:

.. code-block:: bash

    salt-run sdb.get 'sdb://my-bitwarden-vault/by-uuid/2fa63ad5-e4e4-43d4-a089-3fadcf455be2/fields/by-name/test/value'

"""
import logging

import salt.exceptions
import saltext.bitwarden.utils.bitwarden_vault as bitwarden_vault


log = logging.getLogger(__name__)

__func_alias__ = {"set_": "set"}

__virtualname__ = "bitwarden"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The bitwarden sdb module is not implemented yet")
    return __virtualname__


def _get_config(profile=None):  # pylint: disable=C0116
    if profile and profile.get("driver") != "bitwarden":
        log.error("The specified profile is not a bitwarden profile")
        return {}
    elif not profile:
        log.error("The config is not set")
        return {}

    return profile


def delete(key, profile=None):
    """
    Delete a value from a Bitwarden vault item. (Currently not implemented)

    This function only deletes individual values within a vault item, and will
    not delete entire items. To delete items, please use one of the execution,
    runner, or state modules instead.
    """
    raise salt.exceptions.NotImplemented()


def set_(*args, **kwargs):
    """
    Set a value in a Bitwarden vault item. (Currently not implemented)

    This function only sets individual values within a vault item, and will not
    create new items. To create new items, please use one of the execution,
    runner, or state modules instead.
    """
    raise salt.exceptions.NotImplemented()


def get(key, profile=None):
    """
    Get a value from a Bitwarden vault item.

    This function only gets individual values within a vault item, and will not
    retrieve an entire item. To retrieve entire items, please use one of the
    execution, pillar, runner, or state modules instead.
    """
    opts = _get_config(profile=profile)
    args = key.split("/")
    if len(args) != 3 and len(args) != 5 and len(args) != 6:
        log.error("Invalid number of arguments in sdb path.")
        return False
    if args[0] == "by-uuid":
        if args[2] in [
            "name",
            "username",
            "password",
            "totp",
            "notes",
            "creation_date",
            "revision_date",
            "deleted_date",
            "password_revision_date",
        ]:
            item = bitwarden_vault.get_item(opts=opts, item_id=args[1])
            if args[2] == "name":
                return item["name"]
            if args[2] == "username":
                return item["login"]["username"]
            elif args[2] == "password":
                return item["login"]["password"]
            elif args[2] == "totp":
                return bitwarden_vault.get_item_field(opts=opts, item_id=args[1], field="totp")
            elif args[2] == "notes":
                return item["notes"]
            elif args[2] == "creation_date":
                return item["creation_date"]
            elif args[2] == "revision_date":
                return item["revision_date"]
            elif args[2] == "deleted_date":
                return item["deleted_date"]
            elif args[2] == "password_revision_date":
                return item["login"]["password_revision_date"]
        elif args[2] == "password_history" and len(args) == 5:
            if args[3] == "by-index" and args[4].isdigit():
                password_index = int(args[4])
                item = bitwarden_vault.get_item(opts=opts, item_id=args[1])
                value = None
                if password_index == 0:
                    return item["login"]["password"]
                else:
                    if not item.get("password_history") or password_index > len(
                        item["password_history"]
                    ):
                        log.error('Supplied index "%s" exceeds password history', password_index)
                        return None
                    return item["password_history"][password_index - 1]["password"]
            elif args[3] != "by-index":
                log.error('Supplied locator "%s" is invalid', args[3])
                return False
            elif not args[4].isdigit():
                log.error('Supplied index "%s" is not a non-negative integer', args[4])
                return False
        elif args[2] == "fields" and len(args) == 6:
            if args[5] in [
                "value",
                "type",
                "linked_id",
            ]:
                item = bitwarden_vault.get_item(opts=opts, item_id=args[1])
                value = None
                for field in item["fields"]:
                    if field["name"] == args[4]:
                        if value is not None:
                            log.error('Supplied field name "%s" is not unique', args[4])
                            return None
                        else:
                            value = field[args[5]]
                return value
        else:
            log.error(
                'Supplied object "%s" is not one of: "%s".',
                args[2],
                '", "'.join(
                    [
                        "name",
                        "username",
                        "password",
                        "totp",
                        "notes",
                        "creation_date",
                        "revision_date",
                        "deleted_date",
                        "password_revision_date",
                        "password_history",
                        "fields",
                    ]
                ),
            )
            return False
    else:
        log.error('Supplied locator method "%s" is invalid.', args[0])
        return False
    return None
