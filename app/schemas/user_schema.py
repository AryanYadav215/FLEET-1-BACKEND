from pydantic import BaseModel, EmailStr
from typing import Optional


# ---------------- LOGIN ----------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------------- SIGNUP ----------------
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    company_name: Optional[str] = None


# ---------------- UPDATE USER ----------------
class UpdateUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    company_name: Optional[str] = None


# ---------------- RESPONSE SCHEMA ----------------
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    company_name: Optional[str]

    class Config:
        from_attributes = True