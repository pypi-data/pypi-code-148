from enum import Enum

from pydantic import BaseModel

from datagen_protocol.schemas import fields, config
from datagen_protocol.schemas.core.d3 import Point, Rotation


class LightType(str, Enum):
    NIR = "nir"


class Light(BaseModel):
    light_type: LightType
    beam_angle: float = fields.numeric(config.light.beam_angle)
    brightness: float = fields.numeric(config.light.brightness)
    falloff: float = fields.numeric(config.light.falloff)
    location: Point = fields.point(config.light.location)
    rotation: Rotation = fields.rotation(config.light.rotation)
