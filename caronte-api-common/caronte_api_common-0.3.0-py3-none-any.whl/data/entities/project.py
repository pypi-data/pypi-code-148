from typing import List, Optional

from pydantic import UUID4, BaseModel

from caronte_common.data.entities.claim import Claim
from caronte_common.data.entities.config import Config
from caronte_common.data.entities.role import Role
from caronte_common.data.entities.user import User


class Project(BaseModel):
    name: str
    description: str
    config: Optional[Config] = None
    claims: Optional[List[Claim]] = None
    roles: Optional[List[Role]] = None
    users: Optional[List[User]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    external_id: Optional[UUID4] = None
