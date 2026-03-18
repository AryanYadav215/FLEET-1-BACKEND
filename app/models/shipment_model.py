from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_code = Column(String)

    manufacturer_id = Column(UUID(as_uuid=True))

    pickup_address = Column(String)
    pickup_city = Column(String)
    pickup_contact = Column(String)

    receiver_name = Column(String)
    receiver_address = Column(String)
    receiver_city = Column(String)
    receiver_phone = Column(String)

    goods_description = Column(String)

    quantity = Column(Integer)
    weight = Column(Float)

    status = Column(String)

    current_transporter_id = Column(UUID(as_uuid=True), nullable=True)