from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import UpdateUser

router = APIRouter(prefix="/users", tags=["Users"])


# ---------------- GET ALL USERS ----------------
@router.get("/")
def get_all_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users


# ---------------- GET USER BY ID ----------------
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ---------------- UPDATE USER ----------------
@router.put("/{user_id}")
def update_user(user_id: int, data: UpdateUser, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # update fields
    user.name = data.name
    user.email = data.email
    user.password = data.password
    user.role = data.role
    user.company_name = data.company_name

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "user": user
    }

# ---------------- DELETE USER ----------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}