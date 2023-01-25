"""
TransferType dataclass and constructor
"""

from dataclasses import dataclass
from multiprocessing import cpu_count
from typing import Optional

from hoppr import constants


@dataclass
class Plugin:
    """
    Plugin Dataclass containing name and optional config
    """

    def __init__(self, name: str, config: Optional[dict] = None) -> None:
        self.name = name
        self.config = config


@dataclass
class Stage:
    """
    Stage Dataclass containing an array of plugins
    """

    def __init__(self, name: str, stage_config: dict) -> None:
        self.name: str = name
        self.component_coverage: Optional[str] = stage_config.get("component_coverage")
        self.plugins: list[Plugin] = []
        for plugin in stage_config.get(constants.ConfigKeys.PLUGINS, []):
            self.plugins.append(Plugin(**plugin))


class TransferFileContent:  # pylint: disable="too-few-public-methods"
    """
    Transfer data type class to construct TransferType Object
    """

    def __init__(
        self,
        schemaVersion: str,  # pylint: disable="invalid-name"
        kind: str,
        stages: dict,
        max_processes: Optional[int] = None,
    ) -> None:
        self.schema_version = schemaVersion
        self.kind = kind
        self.stages = []
        for name, stage in stages.items():
            self.stages.append(Stage(name, stage))

        self.max_processes = cpu_count()
        if max_processes is not None:
            self.max_processes = max_processes
