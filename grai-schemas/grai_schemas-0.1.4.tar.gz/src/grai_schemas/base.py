from typing import Union

from grai_schemas.models import GraiEdgeMetadata, GraiNodeMetadata
from pydantic import BaseModel


class EdgeMetadata(BaseModel):
    grai: GraiEdgeMetadata


class NodeMetadata(BaseModel):
    grai: GraiNodeMetadata


class Metadata(BaseModel):
    grai: Union[GraiNodeMetadata, GraiEdgeMetadata]


