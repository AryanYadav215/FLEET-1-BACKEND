from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import Base


class Transporter(Base):
    __tablename__ = "transporters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    city = Column(String(100))
    route = Column(String(255))
    contact_number = Column(String(20))