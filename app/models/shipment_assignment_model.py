from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class ShipmentAssignment(Base):
    __tablename__ = "shipment_assignments"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    transporter_id = Column(Integer, ForeignKey("transporters.id"))
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_at = Column(TIMESTAMP, server_default=func.now())