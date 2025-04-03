import pytest

@pytest.mark.book
def test_add_book(client):
    """Test adding a new book."""
    response = client.post(
        "/books/",
        json={"title": "Test Book", "author": "Test Author", "isbn": "1234567890"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Book"

@pytest.mark.book
def test_add_book_duplicate_isbn(client):
    """Test adding a book with a duplicate ISBN."""
    client.post("/books/", json={"title": "Book 1", "author": "Author 1", "isbn": "1111111111"})
    response = client.post("/books/", json={"title": "Book 2", "author": "Author 2", "isbn": "1111111111"})
    
    assert response.status_code == 400  
    assert response.json()["detail"] == "Book with this ISBN already exists"

@pytest.mark.book
def test_get_books(client):
    """Test retrieving all books."""
    client.post("/books/", json={"title": "Book A", "author": "Author A", "isbn": "2222222222"})
    client.post("/books/", json={"title": "Book B", "author": "Author B", "isbn": "3333333333"})

    response = client.get("/books/")
    
    assert response.status_code == 200
    assert len(response.json()) >= 2  # Ensure at least two books exist

@pytest.mark.book
def test_get_book_by_id(client):
    """Test retrieving a book by its ID."""
    book_response = client.post("/books/", json={"title": "Unique Book", "author": "Unique Author", "isbn": "4444444444"})
    book_id = book_response.json()["id"]

    response = client.get(f"/books/{book_id}")
    
    assert response.status_code == 200
    assert response.json()["id"] == book_id

@pytest.mark.book
def test_get_nonexistent_book(client):
    """Test retrieving a book that does not exist."""
    response = client.get("/books/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

@pytest.mark.book
def test_update_book(client):
    """Test updating an existing book."""
    book_response = client.post("/books/", json={"title": "Old Title", "author": "Author", "isbn": "5555555555"})
    book_id = book_response.json()["id"]

    update_response = client.put(
        f"/books/{book_id}",
        json={"title": "Updated Title", "author": "Updated Author", "isbn": "5555555555"}
    )

    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"

@pytest.mark.book
def test_update_nonexistent_book(client):
    """Test updating a book that does not exist."""
    response = client.put("/books/999", json={"title": "New Title", "author": "New Author", "isbn": "6666666666"})
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

@pytest.mark.book
def test_delete_book(client):
    """Test deleting a book."""
    book_response = client.post("/books/", json={"title": "Book to Delete", "author": "Author", "isbn": "7777777777"})
    book_id = book_response.json()["id"]

    delete_response = client.delete(f"/books/{book_id}")
    
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Book deleted successfully"

    # Ensure book is actually deleted
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404

@pytest.mark.book
def test_delete_nonexistent_book(client):
    """Test deleting a book that does not exist."""
    response = client.delete("/books/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
