from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid


class ShipmentStatusUpdate(Base):
    __tablename__ = "shipment_status_updates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    shipment_id = Column(UUID(as_uuid=True))
    status = Column(String)

    # FIX: Changed from location to city to match your database
    city = Column(String)

    updated_by = Column(UUID(as_uuid=True))

    created_at = Column(TIMESTAMP, server_default=func.now())