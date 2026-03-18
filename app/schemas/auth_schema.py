from pydantic import BaseModel


class SignupRequest(BaseModel):
    full_name: str
    phone: str
    role: str
    company_name: str
    password: str


class LoginRequest(BaseModel):
    phone: str
    password: str