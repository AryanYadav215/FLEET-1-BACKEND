import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.shipment_model import Shipment
from app.models.transporter_model import Transporter
from app.models.shipment_assignment_model import ShipmentAssignment

router = APIRouter(prefix="/assignments", tags=["Assignments"])

@router.post("/")
def assign_transporter(shipment_id: str, transporter_id: str, assigned_by: str, db: Session = Depends(get_db)):

    shipment_uuid = uuid.UUID(shipment_id)
    transporter_uuid = uuid.UUID(transporter_id)

    shipment = db.query(Shipment).filter(Shipment.id == shipment_uuid).first()
    transporter = db.query(Transporter).filter(Transporter.id == transporter_uuid).first()

    if not shipment or not transporter:
        raise HTTPException(status_code=404, detail="Not found")

    assignment = ShipmentAssignment(
        shipment_id=shipment_uuid,
        transporter_id=transporter_uuid,
        assigned_by=uuid.UUID(assigned_by),
        leg_number=1,
        is_current=True
    )

    shipment.current_transporter_id = transporter_uuid

    db.add(assignment)
    db.commit()

    return {"message": "Assigned"}