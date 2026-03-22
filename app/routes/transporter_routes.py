from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserResponse

# 👇 THIS WAS THE MISSING LINE! 👇
router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_transporters(db: Session = Depends(get_db)):
    # Grabs EVERY user where role is 'transporter'
    transporters = db.query(User).filter(User.role == "transporter").all()

    return transporters