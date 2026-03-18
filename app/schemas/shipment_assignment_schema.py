from pydantic import BaseModel


class AssignmentCreate(BaseModel):
    shipment_id: str
    transporter_id: str
    assigned_by: str