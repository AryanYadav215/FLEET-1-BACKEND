from pydantic import BaseModel


class StatusCreate(BaseModel):
    shipment_id: str
    status: str
    location: str
    updated_by: str