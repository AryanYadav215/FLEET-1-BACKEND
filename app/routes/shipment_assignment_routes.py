from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.models.shipment_model import Shipment
from app.schemas.shipment_schema import ShipmentCreate

router = APIRouter()


@router.post("/shipments")
def create_shipment(data: ShipmentCreate, db: Session = Depends(get_db)):

    # Check user exists
    user = db.query(User).filter(User.id == data.manufacturer_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check role
    if user.role != "MANUFACTURER":
        raise HTTPException(
            status_code=400,
            detail="User is not a manufacturer"
        )

    shipment = Shipment(
        manufacturer_id=data.manufacturer_id,
        pickup_address=data.pickup_address,
        pickup_city=data.pickup_city,
        pickup_contact=data.pickup_contact,
        delivery_address=data.delivery_address,
        delivery_city=data.delivery_city,
        receiver_name=data.receiver_name,
        receiver_phone=data.receiver_phone,
        goods_description=data.goods_description,
        quantity=data.quantity,
        weight=data.weight,
        type_goods=data.type_goods,
        status="CREATED"
    )

    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    return shipment