from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    cellphone: str
    user_name: str
    full_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    password: Optional[str] = None
    external_id: Optional[UUID] = None
