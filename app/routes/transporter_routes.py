from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserResponse

# ✅ FIX: Added prefix and tags
router = APIRouter(
    prefix="/transporters",
    tags=["Transporters"]
)

# ===============================
# GET ALL TRANSPORTERS
# ===============================
@router.get("/", response_model=List[UserResponse])
def get_transporters(db: Session = Depends(get_db)):
    transporters = db.query(User).filter(User.role == "transporter").all()
    return transporters