from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ==========================================
# 1. Schemas for Shipment Events (Timeline)
# ==========================================

# What we return when someone asks for the timeline
class ShipmentEventResponse(BaseModel):
    id: int
    shipment_id: int
    status: Optional[str] = None
    location: Optional[str] = None
    updated_by: Optional[int] = None
    event_time: Optional[datetime] = None

    class Config:
        from_attributes = True  # Tells Pydantic to read data from SQLAlchemy models

# ==========================================
# 2. Schemas for Shipments
# ==========================================

# What the user sends to CREATE a new shipment
class ShipmentCreate(BaseModel):
    tracking_number: str
    # We don't ask for ID or status here, because ID is auto-generated
    # and status defaults to "Created" in the database.

# What we return when someone views a shipment (or lists shipments)
class ShipmentResponse(BaseModel):
    id: int
    tracking_number: str
    status: str

    class Config:
        from_attributes = True

# What the user sends to UPDATE an existing shipment
class ShipmentUpdate(BaseModel):
    status: Optional[str] = None