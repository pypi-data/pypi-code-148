from typing import List

from datagen_protocol import __version__ as __datagen_protocol_version__
from datagen_protocol.schemas.core.humans import HumanDatapoint
from pydantic import BaseModel


class DataRequest(BaseModel):
    __protocol_version__: str = __datagen_protocol_version__

    datapoints: List[HumanDatapoint]
