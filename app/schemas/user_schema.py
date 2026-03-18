from pydantic import BaseModel
from typing import Optional


# ===============================
# RESPONSE SCHEMA (for API output)
# ===============================
class UserResponse(BaseModel):
    id: str
    full_name: str
    phone: str
    role: str
    company_name: Optional[str]

    class Config:
        from_attributes = True


# ===============================
# UPDATE SCHEMA
# ===============================
class UpdateUser(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    company_name: Optional[str] = None
    password: Optional[str] = None