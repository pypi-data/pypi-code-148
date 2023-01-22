from typing import Optional, Union
from pydantic import UUID4, BaseModel


class Claim(BaseModel):
    name: str
    value: Union[str, int, float]
    external_id: Optional[UUID4] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
