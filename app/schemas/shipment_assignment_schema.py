from pydantic import BaseModel

class ShipmentAssignmentCreate(BaseModel):
    shipment_id: int
    transporter_id: int
    assigned_by: int


class ShipmentAssignmentUpdate(BaseModel):
    transporter_id: int