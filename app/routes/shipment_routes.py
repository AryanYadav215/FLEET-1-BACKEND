import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.shipment_model import Shipment
from app.schemas.shipment_schema import ShipmentCreate

router = APIRouter(prefix="/shipments", tags=["Shipments"])

@router.post("/")
def create_shipment(data: ShipmentCreate, db: Session = Depends(get_db)):
    shipment = Shipment(
        shipment_code=data.shipment_code,
        manufacturer_id=uuid.UUID(data.manufacturer_id),

        pickup_address=data.pickup_address,
        pickup_city=data.pickup_city,
        pickup_contact=data.pickup_contact,

        receiver_name=data.receiver_name,
        receiver_address=data.receiver_address,
        receiver_city=data.receiver_city,
        receiver_phone=data.receiver_phone,

        goods_description=data.goods_description,
        quantity=data.quantity,
        weight=data.weight,
        status="CREATED"
    )

    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    return shipment

@router.get("/")
def get_all_shipments(db: Session = Depends(get_db)):
    return db.query(Shipment).all()