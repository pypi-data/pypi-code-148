from enum import Enum
from typing import Optional

from pydantic import BaseModel

from datagen_protocol.schemas import fields, config


class LensColor(str, Enum):
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    BLACK = "black"
    RED = "red"


class FrameColor(str, Enum):
    BLACK = "black"
    WHITE = "white"
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    GRAY = "gray"
    SILVER = "silver"
    GOLD = "gold"


class GlassesPosition(str, Enum):
    ON_NOSE = "on_nose"


class Glasses(BaseModel):
    id: str
    lens_color: LensColor = fields.enum(LensColor, config.accessories.glasses.lens.color)
    lens_reflectivity: float = fields.numeric(config.accessories.glasses.lens.reflectivity)
    lens_transparency: float = fields.numeric(config.accessories.glasses.lens.transparency)
    frame_color: FrameColor = fields.enum(FrameColor, config.accessories.glasses.frame.color)
    frame_metalness: float = fields.numeric(config.accessories.glasses.frame.metalness)
    position: GlassesPosition = fields.enum(GlassesPosition, config.accessories.glasses.position)


class MaskColor(str, Enum):
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    BLACK = "black"
    RED = "red"


class MaskPosition(str, Enum):
    ON_NOSE = "on_nose"
    ON_MOUTH = "on_mouth"
    ON_CHIN = "on_chin"


class MaskTexture(str, Enum):
    CLOTH = "cloth"
    DIAMOND_PATTERN = "diamond_pattern"
    WOVEN = "woven"


class Mask(BaseModel):
    id: str
    color: MaskColor = fields.enum(MaskColor, config.accessories.mask.color)
    texture: MaskTexture = fields.enum(MaskTexture, config.accessories.mask.texture)
    position: MaskPosition = fields.enum(MaskPosition, config.accessories.mask.position)
    roughness: float = fields.numeric(config.accessories.mask.roughness)


class Accessories(BaseModel):
    glasses: Optional[Glasses]
    mask: Optional[Mask]
