from pydantic import BaseModel
from typing import Optional


# ===============================
# CREATE SCHEMA
# ===============================
class TransporterCreate(BaseModel):
    user_id: str
    company_name: str
    operating_city: str
    service_routes: Optional[str] = None
    contact_person: str
    phone: str


# ===============================
# UPDATE SCHEMA
# ===============================
class TransporterUpdate(BaseModel):
    company_name: Optional[str] = None
    operating_city: Optional[str] = None
    service_routes: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


# ===============================
# RESPONSE SCHEMA
# ===============================
class TransporterResponse(BaseModel):
    id: str
    user_id: str
    company_name: str
    operating_city: str
    service_routes: Optional[str]
    contact_person: str
    phone: str
    is_active: bool

    class Config:
        from_attributes = True