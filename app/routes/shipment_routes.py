from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import your database session, models, and schemas
from app.database import SessionLocal
from app.models import shipment_model
from app.schemas import shipment_schema

# Set up the router
router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"]
)


# Database Dependency: This safely opens and closes a database connection for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# 1. POST /shipments - Create a new shipment
# ==========================================
@router.post("/", response_model=shipment_schema.ShipmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment(shipment: shipment_schema.ShipmentCreate, db: Session = Depends(get_db)):
    # First, let's check if a shipment with this tracking number already exists
    # to prevent database crash errors!
    existing_shipment = db.query(shipment_model.Shipment).filter(
        shipment_model.Shipment.tracking_number == shipment.tracking_number
    ).first()

    if existing_shipment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A shipment with this tracking number already exists."
        )

    # Convert the Pydantic schema data into a SQLAlchemy database model
    new_shipment = shipment_model.Shipment(
        tracking_number=shipment.tracking_number,
        status="Created"  # Setting the default initial status
    )

    # Save it to the database
    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)  # This grabs the newly generated ID from the database

    return new_shipment


# ==========================================
# 2. GET /shipments - List all shipments
# ==========================================
@router.get("/", response_model=List[shipment_schema.ShipmentResponse])
def get_all_shipments(db: Session = Depends(get_db)):
    # This query fetches every single shipment from the database
    shipments = db.query(shipment_model.Shipment).all()

    return shipments


# ==========================================
# 3. GET /shipments/{id} - Get a single shipment
# ==========================================
@router.get("/{shipment_id}", response_model=shipment_schema.ShipmentResponse)
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    # Query the database for a shipment with this specific ID
    shipment = db.query(shipment_model.Shipment).filter(shipment_model.Shipment.id == shipment_id).first()

    # If the database comes back empty, tell the user it wasn't found (404 Error)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found."
        )

    return shipment


# ==========================================
# 4. GET /shipments/{id}/timeline - Get shipment timeline
# ==========================================
@router.get("/{shipment_id}/timeline", response_model=List[shipment_schema.ShipmentEventResponse])
def get_shipment_timeline(shipment_id: int, db: Session = Depends(get_db)):
    # 1. First, let's verify the shipment actually exists
    shipment = db.query(shipment_model.Shipment).filter(shipment_model.Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found."
        )

    # 2. Fetch all events for this shipment, ordered by newest first
    events = db.query(shipment_model.ShipmentEvent).filter(
        shipment_model.ShipmentEvent.shipment_id == shipment_id
    ).order_by(shipment_model.ShipmentEvent.event_time.desc()).all()

    return events


# ==========================================
# 5. PUT /shipments/{id} - Update a shipment
# ==========================================
@router.put("/{shipment_id}", response_model=shipment_schema.ShipmentResponse)
def update_shipment(
        shipment_id: int,
        shipment_update: shipment_schema.ShipmentUpdate,
        db: Session = Depends(get_db)
):
    # 1. Find the shipment in the database
    shipment = db.query(shipment_model.Shipment).filter(shipment_model.Shipment.id == shipment_id).first()

    # 2. If it doesn't exist, return a 404 error
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found."
        )

    # 3. If a new status was provided, update it
    if shipment_update.status is not None:
        shipment.status = shipment_update.status

        # (Optional but recommended) We can also automatically log this as an event in the timeline!
        new_event = shipment_model.ShipmentEvent(
            shipment_id=shipment.id,
            status=shipment.status
        )
        db.add(new_event)

    # 4. Save the changes to the database
    db.commit()
    db.refresh(shipment)

    return shipment


# ==========================================
# 6. DELETE /shipments/{id} - Delete a shipment
# ==========================================
@router.delete("/{shipment_id}")
def delete_shipment(shipment_id: int, db: Session = Depends(get_db)):
    # 1. Find the shipment
    shipment = db.query(shipment_model.Shipment).filter(shipment_model.Shipment.id == shipment_id).first()

    # 2. If it doesn't exist, return a 404 error
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found."
        )

    # 3. Delete any timeline events attached to this shipment first (Safety rule)
    db.query(shipment_model.ShipmentEvent).filter(
        shipment_model.ShipmentEvent.shipment_id == shipment_id
    ).delete()

    # 4. Now delete the actual shipment
    db.delete(shipment)
    db.commit()

    return {"detail": f"Shipment {shipment_id} has been successfully deleted."}