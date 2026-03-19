from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Handover(Base):
    __tablename__ = "handovers"   # ✅ MUST match your DB table name

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    shipment_id = Column(UUID(as_uuid=True))
    from_transporter_id = Column(UUID(as_uuid=True))
    to_transporter_id = Column(UUID(as_uuid=True))

    handover_city = Column(String)
    handed_over_by = Column(UUID(as_uuid=True))

    created_at = Column(TIMESTAMP, server_default=func.now())