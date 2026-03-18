from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transporter_model import Transporter
from app.schemas.transporter_schema import TransporterCreate, TransporterUpdate

router = APIRouter(prefix="/transporters", tags=["Transporters"])


# CREATE TRANSPORTER
@router.post("/")
def create_transporter(data: TransporterCreate, db: Session = Depends(get_db)):

    transporter = Transporter(
        name=data.name,
        city=data.city,
        route=data.route,
        contact_number=data.contact_number
    )

    db.add(transporter)
    db.commit()
    db.refresh(transporter)

    return transporter


# GET ALL TRANSPORTERS
@router.get("/")
def get_transporters(db: Session = Depends(get_db)):
    return db.query(Transporter).all()


# GET TRANSPORTER BY ID
@router.get("/{transporter_id}")
def get_transporter(transporter_id: int, db: Session = Depends(get_db)):

    transporter = db.query(Transporter).filter(
        Transporter.id == transporter_id
    ).first()

    if not transporter:
        raise HTTPException(status_code=404, detail="Transporter not found")

    return transporter


# UPDATE TRANSPORTER
@router.put("/{transporter_id}")
def update_transporter(transporter_id: int, data: TransporterUpdate, db: Session = Depends(get_db)):

    transporter = db.query(Transporter).filter(
        Transporter.id == transporter_id
    ).first()

    if not transporter:
        raise HTTPException(status_code=404, detail="Transporter not found")

    if data.name:
        transporter.name = data.name
    if data.contact_number:
        transporter.contact_number = data.contact_number
    if data.company_name:
        transporter.company_name = data.company_name

    db.commit()
    db.refresh(transporter)

    return transporter


# DELETE TRANSPORTER
@router.delete("/{transporter_id}")
def delete_transporter(transporter_id: int, db: Session = Depends(get_db)):

    transporter = db.query(Transporter).filter(
        Transporter.id == transporter_id
    ).first()

    if not transporter:
        raise HTTPException(status_code=404, detail="Transporter not found")

    db.delete(transporter)
    db.commit()

    return {"message": "Transporter deleted successfully"}