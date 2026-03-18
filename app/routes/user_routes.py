import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import UpdateUser

router = APIRouter(prefix="/users", tags=["Users"])


# ---------------- GET ALL USERS ----------------
@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# ---------------- GET USER BY ID ----------------
@router.get("/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):

    try:
        user_uuid = uuid.UUID(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid UUID")

    user = db.query(User).filter(User.id == user_uuid).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ---------------- UPDATE USER ----------------
@router.put("/{user_id}")
def update_user(user_id: str, data: UpdateUser, db: Session = Depends(get_db)):

    try:
        user_uuid = uuid.UUID(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid UUID")

    user = db.query(User).filter(User.id == user_uuid).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # update fields (only if provided)
    if data.name is not None:
        user.name = data.name

    if data.email is not None:
        user.email = data.email

    if data.password is not None:
        user.password = data.password

    if data.role is not None:
        user.role = data.role

    if data.company_name is not None:
        user.company_name = data.company_name

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "user": user
    }


# ---------------- DELETE USER ----------------
@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):

    try:
        user_uuid = uuid.UUID(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid UUID")

    user = db.query(User).filter(User.id == user_uuid).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}