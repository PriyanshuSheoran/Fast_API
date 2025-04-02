from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import UserResponse, UserCreate, UserUpdate
from app.dependencies import get_db, get_current_user, hash_password

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_user_profile(current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    if user_update.password:
        user.password_hash = hash_password(user_update.password)
    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    db.commit()
    db.refresh(user)
    return user