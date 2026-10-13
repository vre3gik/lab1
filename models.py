from exceptions import (
    BookAlreadyExistsError,
    BookNotAvailableError,
    BookNotFoundError,
    ReaderAlreadyExistsError,
    ReaderNotFoundError,
)


class Book:
    def __init__(self, id, title, author, available=True):
        self.id = id
        self.title = title
        self.author = author
        self.available = available

    def to_dict(self):
        return {
            "type": "Book",
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "available": self.available,
        }

    def __str__(self):
        status = "свободна" if self.available else "выдана"
        return f"[{self.id}] «{self.title}» — {self.author} ({status})"


class EBook(Book):
    def __init__(self, id, title, author, size_mb, format, available=True):
        super().__init__(id, title, author, available)
        self.size_mb = size_mb
        self.format = format

    def to_dict(self):
        d = super().to_dict()
        d.update({"type": "EBook", "size_mb": self.size_mb, "format": self.format})
        return d

    def __str__(self):
        return super().__str__() + f" [эл. {self.format}, {self.size_mb} МБ]"


class Reader:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.taken = []

    def borrow(self, book):
        if not book.available:
            raise BookNotAvailableError(book.id)
        book.available = False
        self.taken.append(book)

    def give_back(self, book):
        if book in self.taken:
            self.taken.remove(book)
            book.available = True

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "taken_ids": [b.id for b in self.taken],
        }

    def __str__(self):
        return f"[{self.id}] {self.name} (взято: {len(self.taken)})"


class Library:
    def __init__(self, name="Библиотека"):
        self.name = name
        self.books = []
        self.readers = []

    def add_book(self, book):
        if any(b.id == book.id for b in self.books):
            raise BookAlreadyExistsError(book.id)
        self.books.append(book)

    def find_book(self, book_id):
        for b in self.books:
            if b.id == book_id:
                return b
        raise BookNotFoundError(book_id)

    def add_reader(self, reader):
        if any(r.id == reader.id for r in self.readers):
            raise ReaderAlreadyExistsError(reader.id)
        self.readers.append(reader)

    def find_reader(self, reader_id):
        for r in self.readers:
            if r.id == reader_id:
                return r
        raise ReaderNotFoundError(reader_id)

    def lend(self, book_id, reader_id):
        book = self.find_book(book_id)
        reader = self.find_reader(reader_id)
        reader.borrow(book)

    def give_back(self, book_id, reader_id):
        book = self.find_book(book_id)
        reader = self.find_reader(reader_id)
        reader.give_back(book)

    def __str__(self):
        return f"«{self.name}» (книг: {len(self.books)}, читателей: {len(self.readers)})"
