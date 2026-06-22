from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Library API")


# Модель данных для книги
class Book(BaseModel):
    id: int
    title: str
    author: str
    is_borrowed: bool = False


# Имитация базы данных в памяти
fake_db = []


@app.get("/")
def read_root():
    return {"message": "Welcome to the Library API. Go to /docs to test the endpoints."}


@app.get("/books", response_model=list[Book])
def get_books():
    """Возвращает список всех книг."""
    return fake_db


@app.post("/books", response_model=Book, status_code=201)
def add_book(book: Book):
    """Добавляет новую книгу в библиотеку."""
    if any(b.id == book.id for b in fake_db):
        raise HTTPException(status_code=400, detail="Book with this ID already exists")

    fake_db.append(book)
    return book


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    """Получает информацию о конкретной книге по её ID."""
    for book in fake_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")
