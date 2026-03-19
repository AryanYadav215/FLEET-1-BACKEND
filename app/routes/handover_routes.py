import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.handover_model import Handover
from app.models.shipment_model import Shipment
from app.models.transporter_model import Transporter
from app.models.user_model import User
from app.schemas.handover_schema import HandoverCreate, HandoverResponse

router = APIRouter(prefix="/handovers", tags=["Handovers"])


# ===============================
# CREATE HANDOVER
# ===============================
@router.post("/", response_model=HandoverResponse)
def create_handover(data: HandoverCreate, db: Session = Depends(get_db)):

    shipment_uuid = data.shipment_id
    from_uuid = data.from_transporter_id
    to_uuid = data.to_transporter_id
    user_uuid = data.handed_over_by

    # check shipment
    if not db.query(Shipment).filter(Shipment.id == shipment_uuid).first():
        raise HTTPException(status_code=404, detail="Shipment not found")

    # check transporters
    if not db.query(Transporter).filter(Transporter.id == from_uuid).first():
        raise HTTPException(status_code=404, detail="From transporter not found")

    if not db.query(Transporter).filter(Transporter.id == to_uuid).first():
        raise HTTPException(status_code=404, detail="To transporter not found")

    # check user
    if not db.query(User).filter(User.id == user_uuid).first():
        raise HTTPException(status_code=404, detail="User not found")

    handover = Handover(
        shipment_id=shipment_uuid,
        from_transporter_id=from_uuid,
        to_transporter_id=to_uuid,
        handover_city=data.handover_city,
        handed_over_by=user_uuid
    )

    db.add(handover)
    db.commit()
    db.refresh(handover)

    return handover