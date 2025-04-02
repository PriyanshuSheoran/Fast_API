from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Book, BorrowHistory, User
from app.schemas import BookResponse, BorrowResponse
from app.dependencies import get_current_user
from datetime import datetime

router = APIRouter()

# User Endpoints
@router.get("/", response_model=list[BookResponse])
def browse_books(db: Session = Depends(get_db)):
    """View all available books."""
    return db.query(Book).all()

@router.post("/{id}/borrow")
def borrow_book(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Borrow a book if available."""
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    borrow_record = BorrowHistory(user_id=current_user.id, book_id=id, borrowed_at=datetime.utcnow())
    db.add(borrow_record)
    db.commit()
    return {"message": "Book borrowed successfully"}

@router.post("/{id}/return")
def return_book(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Return a borrowed book."""
    borrow_record = db.query(BorrowHistory).filter(
        BorrowHistory.user_id == current_user.id, BorrowHistory.book_id == id, BorrowHistory.returned_at == None
    ).first()
    if not borrow_record:
        raise HTTPException(status_code=404, detail="No active borrow record found")
    borrow_record.returned_at = datetime.utcnow()
    db.commit()
    return {"message": "Book returned successfully"}

@router.get("/history", response_model=list[BorrowResponse])
def view_borrow_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """View the borrowing history of the current user."""
    return db.query(BorrowHistory).filter(BorrowHistory.user_id == current_user.id).all()
