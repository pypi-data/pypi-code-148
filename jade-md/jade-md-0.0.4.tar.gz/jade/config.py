"""Access configuration variables."""
from __future__ import annotations

import typing

import yaml


def get_config() -> typing.Dict[str, typing.Any]:
    """Get the configuration variables."""
    try:
        with open(".jade-config.yaml") as file:
            return yaml.safe_load(file)
    except Exception:
        return {"site": {"name": "My Site"}}
