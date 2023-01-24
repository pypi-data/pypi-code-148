import abc
from typing import TypeVar, Type

import numpy as np
from pydantic import BaseModel, Field

from datagen_protocol.schemas import config


class Coords3D(BaseModel):
    x: float = Field(ge=config.d3.boundries.min, le=config.d3.boundries.max)
    y: float = Field(ge=config.d3.boundries.min, le=config.d3.boundries.max)
    z: float = Field(ge=config.d3.boundries.min, le=config.d3.boundries.max)


class Point(Coords3D):
    pass


class Vector(Coords3D):
    pass


class Rotation(BaseModel):
    yaw: float
    roll: float
    pitch: float
