import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.shipment_model import Shipment
from app.models.shipment_status_model import ShipmentStatusUpdate
from app.models.user_model import User

router = APIRouter(prefix="/status", tags=["Shipment Status"])


# ===============================
# ADD STATUS UPDATE
# ===============================
@router.post("/")
def add_status(
    shipment_id: str,
    status: str,
    location: str,
    updated_by: str,
    db: Session = Depends(get_db)
):

    # ✅ Convert UUIDs
    try:
        shipment_uuid = uuid.UUID(shipment_id)
        user_uuid = uuid.UUID(updated_by)
    except:
        raise HTTPException(status_code=400, detail="Invalid UUID")

    # ✅ Check shipment exists
    shipment = db.query(Shipment).filter(Shipment.id == shipment_uuid).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    # ✅ Check user exists
    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Create status update
    new_status = ShipmentStatusUpdate(
        shipment_id=shipment_uuid,
        status=status,
        location=location,
        updated_by=user_uuid
    )

    db.add(new_status)

    # ✅ ALSO update shipment current status
    shipment.status = status

    db.commit()
    db.refresh(new_status)

    return {
        "message": "Status updated successfully",
        "status_update": new_status
    }


# ===============================
# GET STATUS HISTORY
# ===============================
@router.get("/{shipment_id}")
def get_status_history(shipment_id: str, db: Session = Depends(get_db)):

    try:
        shipment_uuid = uuid.UUID(shipment_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid UUID")

    updates = db.query(ShipmentStatusUpdate).filter(
        ShipmentStatusUpdate.shipment_id == shipment_uuid
    ).order_by(
        ShipmentStatusUpdate.created_at.desc()
    ).all()

    return updates