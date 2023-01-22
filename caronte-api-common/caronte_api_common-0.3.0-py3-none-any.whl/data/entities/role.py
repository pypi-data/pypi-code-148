from typing import List, Optional

from pydantic import UUID4, BaseModel


class Role(BaseModel):
    name: str
    claims: List[UUID4]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
