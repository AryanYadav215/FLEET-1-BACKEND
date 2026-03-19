from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class HandoverCreate(BaseModel):
    shipment_id: UUID
    from_transporter_id: UUID
    to_transporter_id: UUID
    handover_city: str
    handed_over_by: UUID


class HandoverResponse(BaseModel):
    id: UUID
    shipment_id: UUID
    from_transporter_id: UUID
    to_transporter_id: UUID
    handover_city: str
    handed_over_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True