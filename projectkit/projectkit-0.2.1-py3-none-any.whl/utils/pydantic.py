from functools import cached_property

from pydantic import BaseModel


class CPModel(BaseModel):
    class Config:
        keep_untouched = (cached_property,)
