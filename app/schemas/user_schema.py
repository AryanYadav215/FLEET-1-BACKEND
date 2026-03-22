from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    phone: str
    role: str
    company_name: Optional[str] = None
    operating_city: Optional[str] = None
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True