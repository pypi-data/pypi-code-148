from enum import Enum
from typing import Optional, List

from pydantic import Field, BaseModel

from datagen_protocol.schemas import fields, config
from datagen_protocol.schemas.core.d3 import Point, Vector, Rotation
from datagen_protocol.schemas.core.humans.accessories import Accessories
from datagen_protocol.schemas.core.environment import Camera, Background, Light


class HairColor(BaseModel):
    melanin: float = fields.numeric(config.human.hair.melanin)
    redness: float = fields.numeric(config.human.hair.redness)
    whiteness: float = fields.numeric(config.human.hair.whiteness)
    roughness: float = fields.numeric(config.human.hair.roughness)
    index_of_refraction: float = fields.numeric(config.human.hair.refraction)


class Hair(BaseModel):
    id: str
    color_settings: HairColor = Field(default_factory=HairColor)


class Gaze(BaseModel):
    distance: float = fields.numeric(config.human.eyes.gaze.distance)
    direction: Vector = fields.vector(config.human.eyes.gaze.direction)


class Eyes(BaseModel):
    id: str
    target_of_gaze: Gaze = Field(default_factory=Gaze)
    eyelid_closure: float = fields.numeric(config.human.eyes.eyelid_closure)


class ExpressionName(str, Enum):
    NEUTRAL = "none"
    HAPPINESS = "happiness"
    SADNESS = "sadness"
    SURPRISE = "surprise"
    FEAR = "fear"
    ANGER = "anger"
    DISGUST = "disgust"
    CONTEMPT = "contempt"
    MOUTH_OPEN = "mouth_open"


class Expression(BaseModel):
    name: ExpressionName = fields.enum(ExpressionName, config.human.expression.name)
    intensity: float = fields.numeric(config.human.expression.intensity)


class Head(BaseModel):
    eyes: Eyes
    hair: Optional[Hair]
    eyebrows: Optional[Hair]
    facial_hair: Optional[Hair]
    expression: Expression = Field(default_factory=Expression)
    location: Point = fields.point(config.human.head.location)
    rotation: Rotation = fields.rotation(config.human.head.rotation)


class Human(BaseModel):
    id: str
    head: Head


class HumanDatapoint(BaseModel):
    human: Human
    camera: Camera
    accessories: Optional[Accessories]
    background: Optional[Background]
    lights: Optional[List[Light]]
