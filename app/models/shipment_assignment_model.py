from sqlalchemy import Column, Integer, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid

class ShipmentAssignment(Base):
    __tablename__ = "shipment_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    shipment_id = Column(UUID(as_uuid=True))
    transporter_id = Column(UUID(as_uuid=True))
    assigned_by = Column(UUID(as_uuid=True))

    leg_number = Column(Integer)
    is_current = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())