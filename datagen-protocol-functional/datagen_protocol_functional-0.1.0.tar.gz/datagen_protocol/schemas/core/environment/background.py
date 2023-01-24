from pydantic import BaseModel

from datagen_protocol.schemas import fields, config


class Background(BaseModel):
    id: str
    rotation: float = fields.numeric(config.background.rotation)
    transparent: bool = fields.bool(config.background.transparency)
