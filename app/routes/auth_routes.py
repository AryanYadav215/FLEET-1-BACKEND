from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

# Import both Models
from app.models.user_model import User
from app.models.transporter_model import Transporter

# Import both Schemas
from app.schemas.auth_schema import SignupRequest, LoginRequest

router = APIRouter(tags=["Auth"])

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    # 1. Check if user exists
    existing_user = db.query(User).filter(User.phone == data.phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # 2. Create User in 'profiles' (maps all address fields automatically)
    new_user = User(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 3. If Transporter, create link in 'transporters' table
    if new_user.role == "transporter":
        new_transporter = Transporter(
            user_id=new_user.id,
            company_name=new_user.company_name,
            operating_city=new_user.city # Using 'city' from signup for logistics
        )
        db.add(new_transporter)
        db.commit()

    return {"message": "User created", "user_id": str(new_user.id)}

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == data.phone).first()

    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "user_id": str(user.id),
        "role": user.role
    }