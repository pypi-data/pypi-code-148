from enum import Enum

from pydantic import Field, BaseModel

from datagen_protocol.schemas import fields, config
from datagen_protocol.schemas.core.d3 import Point, Rotation


class Projection(str, Enum):
    PERSPECTIVE = "perspective"
    PANORAMIC = "panoramic"
    ORTHOGRAPHIC = "orthographic"


class Wavelength(str, Enum):
    VISIBLE = "visible"
    NIR = "nir"


class IntrinsicParams(BaseModel):
    projection: Projection = fields.enum(Projection, config.camera.projection)
    wavelength: Wavelength = fields.enum(Wavelength, config.camera.wavelength)
    resolution_height: int = fields.numeric(config.camera.res.height)
    resolution_width: int = fields.numeric(config.camera.res.width)
    fov_horizontal: int = fields.numeric(config.camera.fov.horizontal)
    fov_vertical: int = fields.numeric(config.camera.fov.vertical)
    sensor_width: float = fields.numeric(config.camera.sensor.width)


class ExtrinsicParams(BaseModel):
    location: Point = fields.point(config.camera.location)
    rotation: Rotation = fields.rotation(config.camera.rotation)


class Camera(BaseModel):
    name: str = config.camera.name
    extrinsic_params: ExtrinsicParams = Field(default_factory=ExtrinsicParams)
    intrinsic_params: IntrinsicParams = Field(default_factory=IntrinsicParams)

    @property
    def extrinsics(self) -> ExtrinsicParams:
        return self.extrinsic_params

    @property
    def intrinsics(self) -> IntrinsicParams:
        return self.intrinsic_params
