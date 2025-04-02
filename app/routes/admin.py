from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, dependencies

router = APIRouter(prefix="/admin", tags=["Admin"])

def is_admin(user: models.User):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

@router.post("/books", response_model=schemas.BookResponse)
def add_book(
    book: schemas.BookCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    is_admin(current_user)
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/books/{id}", response_model=schemas.BookResponse)
def update_book(
    id: int,
    book: schemas.BookUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    is_admin(current_user)
    db_book = db.query(models.Book).filter(models.Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/books/{id}")
def delete_book(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    is_admin(current_user)
    db_book = db.query(models.Book).filter(models.Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}

@router.get("/books", response_model=list[schemas.BookResponse])
def get_all_books(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    is_admin(current_user)
    books = db.query(models.Book).all()
    return books

@router.get("/books/{id}", response_model=schemas.BookResponse)
def get_book_by_id(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    is_admin(current_user)
    db_book = db.query(models.Book).filter(models.Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/borrowed-books", response_model=list[schemas.BorrowResponse])
def get_borrowed_books(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    is_admin(current_user)
    borrowed_books = db.query(models.BorrowHistory).all()
    return borrowed_books
