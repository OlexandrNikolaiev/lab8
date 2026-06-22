from fastapi.testclient import TestClient
from main import app, fake_db

client = TestClient(app)


def setup_function():
    fake_db.clear()


def test_add_book():
    """Тест POST-запроса на добавление книги."""
    response = client.post(
        "/books",
        json={"id": 1, "title": "1984", "author": "George Orwell", "is_borrowed": False}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "1984"
    assert len(fake_db) == 1


def test_get_books_empty():
    """Тест GET-запроса, когда база пуста."""
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []


def test_add_duplicate_book_fails():
    """Тест проверки на уникальность ID."""
    client.post(
        "/books",
        json={"id": 1, "title": "1984", "author": "George Orwell"}
    )

    response = client.post(
        "/books",
        json={"id": 1, "title": "Brave New World", "author": "Aldous Huxley"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Book with this ID already exists"
