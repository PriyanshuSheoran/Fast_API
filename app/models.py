from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)  # ✅ Specify length
    email = Column(String(255), unique=True, nullable=False)  # ✅ Specify length
    password_hash = Column(String(255), nullable=False) 
    role = Column(String(50), nullable=False, default="user")

    borrow_history = relationship("BorrowHistory", back_populates="user")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))  
    author = Column(String(255))  
    published_year = Column(Integer, nullable=True)

    borrow_history = relationship("BorrowHistory", back_populates="book")

class BorrowHistory(Base):
    __tablename__ = "borrow_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrowed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    returned_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="borrow_history")
    book = relationship("Book", back_populates="borrow_history")
