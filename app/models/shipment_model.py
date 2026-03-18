from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(100), unique=True, index=True)
    status = Column(String(100), default="Created")

    events = relationship("ShipmentEvent", back_populates="shipment")


class ShipmentEvent(Base):
    __tablename__ = "shipment_events"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    status = Column(String(100))
    location = Column(String(150))
    updated_by = Column(Integer, ForeignKey("users.id"))
    event_time = Column(DateTime, server_default=func.now())  # <-- Changed to DateTime here

    shipment = relationship("Shipment", back_populates="events")