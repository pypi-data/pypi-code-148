from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from caronte_common.data.entities.project import Project


class Owner(BaseModel):
    email: EmailStr
    cellphone: str
    user_name: str
    full_name: str
    projects: Optional[List[Project]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    password: Optional[str] = None
    external_id: Optional[UUID] = None
