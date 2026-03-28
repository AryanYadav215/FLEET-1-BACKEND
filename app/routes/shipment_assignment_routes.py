from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.shipment_model import Shipment
from app.models.transporter_model import Transporter
from app.models.shipment_assignment_model import ShipmentAssignment

router = APIRouter(prefix="/assignments", tags=["Assignments"])


# Schema to catch the JSON Body from React
class AssignmentCreate(BaseModel):
    shipment_id: str
    transporter_id: str
    assigned_by: str


@router.post("")
def assign_transporter(data: AssignmentCreate, db: Session = Depends(get_db)):
    # Print exactly what React sent us to the terminal
    print(f"📦 Attempting to assign Shipment: {data.shipment_id}")
    print(f"🚚 To Transporter: {data.transporter_id}")

    # 1. Search for Shipment (Letting SQLAlchemy handle the string format)
    shipment = db.query(Shipment).filter(Shipment.id == data.shipment_id).first()
    if not shipment:
        print("❌ ERROR: Shipment ID not found in database!")
        raise HTTPException(status_code=404, detail="Shipment not found in database")

    # 2. Search for Transporter
    transporter = db.query(Transporter).filter(Transporter.id == data.transporter_id).first()
    if not transporter:
        print("❌ ERROR: Transporter ID not found in database!")
        raise HTTPException(status_code=404, detail="Transporter not found in database")

    try:
        # 3. Create Assignment
        assignment = ShipmentAssignment(
            shipment_id=shipment.id,
            transporter_id=transporter.id,
            assigned_by=data.assigned_by,
            leg_number=1,
            is_current=True
        )

        # 4. Update the shipment's current transporter
        shipment.current_transporter_id = transporter.id
        shipment.status = "ASSIGNED"

        db.add(assignment)
        db.commit()

        print("✅ SUCCESS: Transporter Assigned!")
        return {"message": "Assigned successfully"}

    except Exception as e:
        db.rollback()
        print(f"🚨 DB SAVE ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save assignment to database")