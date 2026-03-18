from pydantic import BaseModel
from typing import Optional


class TransporterCreate(BaseModel):
    name: str
    city: str
    route: Optional[str] = None
    contact_number: str


class TransporterUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    route: Optional[str] = None
    contact_number: Optional[str] = None