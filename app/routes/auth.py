from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.utils import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_access_token
from app.dependencies import get_current_user

router = APIRouter()

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/signup", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user.password)
    
    new_user = User(
        email=user.email, 
        username=user.username, 
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user  

@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(
    token_data: RefreshTokenRequest, db: Session = Depends(get_db)
):
    payload = decode_access_token(token_data.refresh_token)
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )
    
    new_access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_user_details(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_details(
    user_update: UserCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if user_update.password:
        current_user.password_hash = get_password_hash(user_update.password)

    current_user.username = user_update.username or current_user.username
    current_user.email = user_update.email or current_user.email
    
    db.commit()
    db.refresh(current_user)
    
    return current_user
