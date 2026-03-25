from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import uuid

# Import both Models
from app.models.user_model import User
from app.models.transporter_model import Transporter

# Import both Schemas
from app.schemas.auth_schema import SignupRequest, LoginRequest

# 👇 THE FIX: Re-added the prefix so frontend calls like /auth/login work again
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    # Normalize phone: remove spaces
    phone_clean = data.phone.strip()
    
    existing_user = db.query(User).filter(User.phone == phone_clean).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        # Create user with a fresh UUID
        user_data = data.dict()
        user_data['phone'] = phone_clean
        new_user = User(**user_data)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # ... (rest of transporter logic)
        
        return {"message": "User created", "user_id": str(new_user.id)}
    except Exception as e:
        db.rollback()
        print(f"SIGNUP ERROR: {str(e)}") # This shows in your terminal
        raise HTTPException(status_code=500, detail="Check database columns match model")

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Use .strip() to avoid space issues
    user = db.query(User).filter(User.phone == data.phone.strip()).first()

    if not user:
        print(f"LOGIN FAIL: Phone {data.phone} not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    if user.password != data.password:
        print(f"LOGIN FAIL: Password mismatch for {data.phone}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "id": str(user.id),
        "full_name": user.full_name,
        "phone": user.phone,
        "role": user.role,
        "company_name": user.company_name,
        "street": user.street,
        "city": user.city,
        "state": user.state,
        "pincode": user.pincode
    }


@router.get("/profile/{user_id}")
def get_profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🚨 UPDATED: Ensuring these match your User model columns
    return {
        "full_name": user.full_name,
        "phone": user.phone,
        "role": user.role,
        "company_name": user.company_name,
        "street": user.street,
        "city": user.city,
        "state": user.state,
        "pincode": user.pincode
    }