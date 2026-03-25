from pydantic import BaseModel
from typing import Optional


class ShipmentCreate(BaseModel):
    shipment_code: Optional[str]
    manufacturer_id: str

    pickup_address: str
    pickup_city: str
    pickup_contact: str
    pickup_pincode: str

    receiver_name: str
    receiver_address: str
    receiver_city: str
    receiver_phone: str
    receiver_pincode: str

    goods_description: Optional[str]

    quantity: int
    weight: float


class ShipmentResponse(BaseModel):
    id: str
    status: str

    class Config:
        from_attributes = True