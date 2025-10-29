from functools import wraps
from typing import List, Optional

from pydantic import BaseModel, EmailStr

class Book(BaseModel):
    title: str
    author: str
    year: int
    available: bool = True
    categories: Optional[List[str]] = None

class User(BaseModel):
    name: str
    email: EmailStr
    membership_id: str

class Library(BaseModel):
    books: List[Book] = []
    users: List[User] = []

    def total_books(self) -> int:
        return len(self.books)

class BookNotAvailable(Exception):
    pass

def log_operations(func):
    @wraps (func)
    def wrapper(*args, **kwargs):
        print(f"Выполнение операции: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Операция '{func.__name__}' завершена")
        return result
    return wrapper

def add_book(library: "Library", book: Book) -> None:
    library.books.append(book)

def find_book(library: "Library", title: str) -> Optional[Book]:
    for book in library.books:
        if book.title == title:
            return book
    return None

def is_book_borrow(library: "Library", title: str) -> None:
    book = find_book(library, title)
    if not book:
        raise ValueError(f"Книга '{title}' не найдена.")
    if not book.available:
        raise BookNotAvailable(f"Книга '{title}' уже занята.")
    book.available = False

def return_book(library: "Library", title: str) -> None:
    book = find_book(library, title)
    if not book:
        raise ValueError(f"Книга '{title}' не найдена.")
    book.available = True

if __name__ == "__main__":
    library = Library()

    add_book(library, Book(title="Война и мир", author="Толстой", year=1869, categories=["Классика", "Роман"]))
    add_book(library, Book(title="Руслан и Людмила", author="Пушкин", year=1820, categories=["Поэма"]))
    add_book(library, Book(title="Изучаем Python", author="Лутц", year=2010, categories=["Обучение"]))

    library.users.append(User(name="Иван Иванов", email="ivan@gmail.com", membership_id="U001"))

    print("Всего книг в библиотеке:", library.total_books())

    try:
        is_book_borrow(library, "Изучаем Python")
    except BookNotAvailable as e:
        print("Ошибка:", e)

    try:
        is_book_borrow(library, "Руслан и Людмила")
    except BookNotAvailable as e:
        print("Ошибка:", e)

    try:
        is_book_borrow(library, "Руслан и Людмила")
    except BookNotAvailable as e:
        print("Ошибка:", e)

    return_book(library, "Руслан и Людмила")

    print("Состояние книг:")
    for b in library.books:
        print(f" - {b.title}: {'доступна' if b.available else 'занята'}")


