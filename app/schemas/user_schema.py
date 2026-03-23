from pydantic import BaseModel
from typing import Optional
from uuid import UUID

# 🔹 Response schema
class UserResponse(BaseModel):
    id: UUID
    phone: str
    role: str
    company_name: Optional[str] = None
    operating_city: Optional[str] = None
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True


# 🔥 ADD THIS (IMPORTANT)
class UpdateUser(BaseModel):
    phone: Optional[str] = None
    role: Optional[str] = None
    company_name: Optional[str] = None
    operating_city: Optional[str] = None
    is_active: Optional[bool] = None