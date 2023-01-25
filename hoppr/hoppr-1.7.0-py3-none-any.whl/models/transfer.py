"""
Transfer file data model
"""
from __future__ import annotations

import re

from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Pattern

from pydantic import ConstrainedStr, Field, validator

from hoppr.models.base import HopprBaseModel, HopprBaseSchemaModel
from hoppr.models.types import ComponentCoverage

if TYPE_CHECKING:
    from pydantic.typing import DictStrAny  # pragma: no cover


class StageName(ConstrainedStr):
    """
    Constrained string type for stage key name
    """

    regex: Pattern[str] = re.compile(pattern=r"^[A-Za-z]\w*$")
    min_length: int = 1


class Plugin(HopprBaseModel):
    """
    Plugin data model
    """

    name: str = Field(..., description="Name of plugin")
    config: dict[str, Any] | None = Field(
        None, description="Mapping of additional plugin configuration settings to values"
    )


class Stage(HopprBaseModel):
    """
    Stage data model
    """

    component_coverage: ComponentCoverage | None = Field(
        None, description="Defines how often components should be processed"
    )
    plugins: list[Plugin] = Field(..., description="List of Hoppr plugins to load")


class StageRef(Stage):
    """
    StageRef data model
    """

    name: StageName


class Stages(HopprBaseModel):
    """
    Stages data model
    """

    __root__: dict[StageName, Stage]

    def __iter__(self):
        return iter(self.__root__.items())

    def __getitem__(self, item):
        return self.__root__[item]


class TransferFile(HopprBaseSchemaModel):
    """
    Transfer file data model
    """

    kind: Literal["Transfer", "transfer"]
    max_processes: int | None = Field(3, description="Max processes to create when running Hoppr application")
    stages: Stages = Field(..., description="Mapping of stage names to property definitions")


class Transfer(TransferFile):
    """
    Transfer data model
    """

    @validator("stages", allow_reuse=True)
    @classmethod
    def validate_stages(cls, stages: Stages) -> list[StageRef]:
        """
        Transform Stages into list of StageRef objects
        """
        stage_refs: list[StageRef] = []

        for stage_name, stage in stages:
            stage_dict = stage.dict()
            stage_dict["name"] = stage_name
            stage_refs.append(StageRef.parse_obj(stage_dict))

        return stage_refs

    @classmethod
    def load(cls, source: str | Path | DictStrAny) -> Transfer:
        """
        Load transfer file from local path or dict
        """
        # pylint: disable=duplicate-code
        if isinstance(source, dict):
            return cls.parse_obj(source)

        if isinstance(source, (str, Path)):
            return cls.parse_file(source)

        raise TypeError("'source' argument must be one of: 'str', 'Path', 'dict[str, Any]'")
