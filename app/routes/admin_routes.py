from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.models.shipment_model import Shipment

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    try:
        return {
            "total_users": db.query(User).count(),
            "total_shipments": db.query(Shipment).count(),
            "manufacturers": db.query(User).filter(User.role == "manufacturer").count(),
            "transporters": db.query(User).filter(User.role == "transporter").count(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()