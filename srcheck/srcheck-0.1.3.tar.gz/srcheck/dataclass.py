import re
from typing import Dict, Tuple

import orjson
from pydantic import BaseModel, validator


def orjson_dumps(value, *, default):
    """
    orjson.dumps returns bytes, to match standard json.dumps we need to decode
    """
    return orjson.dumps(value, default=default).decode()


# Create a pydantic model for the datasets
class Dataset(BaseModel):
    """
    A pydantic model for the datasets.
    """

    name: str
    description: str
    path: str
    metadata: str
    hr_sensor: str
    hr_shape: Tuple[int, int, int, int, int]
    hr_url: str
    lr_sensor: str
    lr_shape: Tuple[int, int, int, int, int]
    lr_url: str
    bands: str

    class Config:
        extra = "forbid"
        json_loads = orjson.loads
        json_dumps = orjson_dumps

    @validator("name")
    def check_name(cls, value):
        if re.search(r"\s+", value):
            raise ValueError("name must not contain spaces.")
        return value

    @validator("lr_url", "hr_url", "metadata")
    def check_contributor(cls, value):
        # regex to detect zenodo links
        zenodo_regex = r"(?:https?://)?(?:www[.])?zenodo[.]org/record/[\d]+/?"

        # Check if it is a correct email address or GitHub profile.
        if not re.match(zenodo_regex, value):
            raise ValueError("contributor is neither a GitHub profile nor an email.")
        return value


class SRDatasets(BaseModel):
    SRDatasets: Dict[str, Dataset]
