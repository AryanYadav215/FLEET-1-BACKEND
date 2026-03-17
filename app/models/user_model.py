from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(120), unique=True)
    password = Column(String(255))
    role = Column(String(50))
    company_name = Column(String(150))