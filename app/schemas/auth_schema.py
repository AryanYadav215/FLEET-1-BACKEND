from pydantic import BaseModel
from typing import Optional

class SignupRequest(BaseModel):
    full_name: str
    phone: str
    password: str
    role: str
    company_name: str
    # Detailed address fields
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None

class LoginRequest(BaseModel):
    phone: str
    password: str