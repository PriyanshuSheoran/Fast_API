from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True  # Correct for Pydantic V2

class LoginRequest(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):  # Added UserUpdate schema
    username: Optional[str] = None  # Optional field to update username
    email: Optional[str] = None  # Optional field to update email
    password: Optional[str] = None  # Optional field to update password
    
    class Config:
        from_attributes = True  # Fix for Pydantic V2

class BookCreate(BaseModel):
    title: str
    author: str
    published_year: Optional[int] = None

class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True

class BookUpdate(BaseModel):  
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    sub: str  
    refresh_token: str

class BorrowResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True
