from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
# 👇 1. ADD THIS IMPORT
from app.models.transporter_model import Transporter
from app.schemas.auth_schema import SignupRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone == data.phone).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(**data.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 👇 2. ADD THIS BLOCK (THE PERMANENT FIX)
    if new_user.role == "transporter":
        new_transporter = Transporter(
            user_id=new_user.id,
            company_name=new_user.company_name,
            operating_city="Not Set",
            service_routes="Not Set"
        )
        db.add(new_transporter)
        db.commit()

    return {"message": "User created", "user_id": str(new_user.id)}

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == data.phone).first()

    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user": str(user.id)}