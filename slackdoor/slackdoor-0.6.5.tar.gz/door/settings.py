import os
from importlib import import_module
from pathlib import Path

from case_insensitive_dict import CaseInsensitiveDict


def import_settings(settings_module: str = "local.settings") -> tuple[CaseInsensitiveDict, bool]:
    default_settings = {
        "PLUGINS": [
            "door.plugins.examples.general.PingPongPlugin",
            "door.plugins.examples.general.HelloPlugin",
            "door.plugins.commands.leave.LeaveChannelPlugin",
        ],
    }

    settings = CaseInsensitiveDict[str, str | list | dict | int | tuple](default_settings)

    try:
        local_settings = import_module(settings_module)
        found_local_settings = True
    except ImportError:
        found_local_settings = False
    else:
        for k in dir(local_settings):
            # in case "local_settings.py" executed some code to retrieve stuff from a database
            # or token vault (for example) and then put them in the globals() namespace,only
            # use the things that are "standard" types and don't start with an underscore...
            if not k.startswith("_") and isinstance(v := getattr(local_settings, k), (str, list, dict, int, tuple)):
                settings[k] = v

    for k, v in os.environ.items():
        if k.startswith("DOOR_"):
            settings[k.removeprefix("DOOR_")] = v

    # expand ~'s in setting names that end in _PATH, _FILE or _DIR
    for k, v in settings.items():
        if k.endswith("_PATH") or k.endswith("_FILE") or k.endswith("_DIR"):
            path = Path(v).expanduser()
            path_check = path.parent if k.endswith("_FILE") else path
            if not path_check.exists():
                # no logging configured yet, so just print
                print(f"WARNING: {k} is set to a path which doesn't exist: {path_check}")  # noqa: T201
            settings[k] = str(path)

    return settings, found_local_settings
