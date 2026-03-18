import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transporter_model import Transporter
from app.schemas.transporter_schema import TransporterCreate, TransporterUpdate

router = APIRouter(prefix="/transporters", tags=["Transporters"])

@router.post("/")
def create_transporter(data: TransporterCreate, db: Session = Depends(get_db)):
    transporter = Transporter(
        user_id=uuid.UUID(data.user_id),
        company_name=data.company_name,
        operating_city=data.operating_city,
        service_routes=data.service_routes,
        contact_person=data.contact_person,
        phone=data.phone
    )

    db.add(transporter)
    db.commit()
    db.refresh(transporter)

    return transporter

@router.get("/")
def get_transporters(db: Session = Depends(get_db)):
    return db.query(Transporter).all()