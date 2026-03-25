import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel # 🚨 Added this import

from app.database import get_db
from app.models.shipment_model import Shipment
from app.models.transporter_model import Transporter
from app.models.shipment_assignment_model import ShipmentAssignment

router = APIRouter(prefix="/assignments", tags=["Assignments"])

# 🚨 Create a Schema to catch the JSON Body from React
class AssignmentCreate(BaseModel):
    shipment_id: str
    transporter_id: str
    assigned_by: str

# 🚨 Changed "/" to "" to prevent strict slash 404 errors
@router.post("")
def assign_transporter(data: AssignmentCreate, db: Session = Depends(get_db)):

    shipment_uuid = uuid.UUID(data.shipment_id)
    transporter_uuid = uuid.UUID(data.transporter_id)
    admin_uuid = uuid.UUID(data.assigned_by)

    shipment = db.query(Shipment).filter(Shipment.id == shipment_uuid).first()
    transporter = db.query(Transporter).filter(Transporter.id == transporter_uuid).first()

    if not shipment or not transporter:
        raise HTTPException(status_code=404, detail="Shipment or Transporter not found")

    assignment = ShipmentAssignment(
        shipment_id=shipment_uuid,
        transporter_id=transporter_uuid,
        assigned_by=admin_uuid,
        leg_number=1,
        is_current=True
    )

    # Update the shipment's current transporter
    shipment.current_transporter_id = transporter_uuid
    shipment.status = "ASSIGNED" # Optional: good practice to update status!

    db.add(assignment)
    db.commit()

    return {"message": "Assigned successfully"}