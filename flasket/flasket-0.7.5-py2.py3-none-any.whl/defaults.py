"""
Description
-----------



.. autofunction:: default_configuration

.. data:: SERVER_CFGNAME

Configuration filename default (``flasket.yml``)

.. data:: SERVER_LISTEN

Configuration default listen address (``localhost``)

.. data:: SERVER_PORT

Configuration default listen port (``8080``)

.. data:: CFGFILE_SEARCH_PATHS

Configuration default search paths, uses ``SERVER_CFGNAME``

.. code-block:: python

  [
      ".flasket.yml",
      "flasket.yml",
      "$XDG_CONFIG_HOME/flasket.yml",
      "$HOME/.flasket.yml",
      "/etc/xdg/flasket.yml",
      "/etc/flasket.yml",
  ]

Default configuration
---------------------

.. code-block:: python

  {
      # The following are only used for Flasket configuration before run() is called.
      "cfgname": "flasket.yml",
      "cfgfile_search_paths": [
          ".flasket.yml",
          "flasket.yml",
          "$XDG_CONFIG_HOME/flasket.yml",
          "$HOME/.flasket.yml",
          "/etc/xdg/flasket.yml",
          "/etc/flasket.yml",
      ],
      "description": "Flasket server",
      # The following can be set in the configuration file:
      "server": {
          "debug": False,
          "listen": SERVER_LISTEN,
          "port": SERVER_PORT,
          "ui": True,
          "workers": 0,
          "pidfile": None,
          "proxy": {
              "x_for": 1,
              "x_proto": 1,
              "x_host": 0,
              "x_port": 0,
              "x_prefix": 0,
          },
      },
  }

"""
import os
import typing as t

from boltons.iterutils import flatten_iter, unique_iter
from xdg import XDG_CONFIG_DIRS

SERVER_CFGNAME: str = "flasket.yml"

SERVER_LISTEN: str = "localhost"
SERVER_PORT: int = 8080

# fmt: off
CFGFILE_SEARCH_PATHS: t.List[str] = list(
    unique_iter(
        flatten_iter(
        [
            "./.{cfgname}",                # ./.flasket.yml
            "./{cfgname}",                 # ./flasket.yml
            "$XDG_CONFIG_HOME/{cfgname}",  # ~/.config/flasket.yml
            "~/.{cfgname}",                # ~/.flasket.yml
            [os.path.join(str(e), "{cfgname}") for e in XDG_CONFIG_DIRS],
            "/etc/{cfgname}",              # /etc/flasket.yml
        ],
        ),
    ),
)
# fmt: on


def default_configuration(defaults: t.Dict[t.Any, t.Any] = None) -> t.Dict:
    """
    Convenience function that returns defaults for arguments,
    and for configuration file.

    Parameters
    ----------
    defaults: dict
        a dictionary containing default values.

    Returns
    -------
    dict:
        a dictionary
    """
    defaults = defaults or {}
    defaults["server"] = defaults.get("server") or {}

    # cf. src/middleware/__init__.py
    return {
        "cfgname": defaults.get("cfgname", SERVER_CFGNAME),
        "cfgfile_search_paths": defaults.get("cfgfile_search_paths", CFGFILE_SEARCH_PATHS),
        "description": defaults.get("description", "Flasket server"),
        "server": {
            "rootpath": defaults.get("rootpath"),
            "debug": defaults["server"].get("debug", False),
            "listen": defaults["server"].get("listen", SERVER_LISTEN),
            "port": defaults["server"].get("port", SERVER_PORT),
            "ui": defaults["server"].get("ui", True),
            "workers": defaults["server"].get("workers", 0),
            "pidfile": defaults["server"].get("pidfile", None),
            "proxy": {
                "x_for": defaults["server"].get("proxy", {}).get("x_for", 1),
                "x_proto": defaults["server"].get("proxy", {}).get("x_proto", 1),
                "x_host": defaults["server"].get("proxy", {}).get("x_host", 0),
                "x_port": defaults["server"].get("proxy", {}).get("x_port", 0),
                "x_prefix": defaults["server"].get("proxy", {}).get("x_prefix", 0),
            },
        },
    }
