class LibraryError(Exception):
    pass


class BookAlreadyExistsError(LibraryError):
    def __init__(self, book_id):
        super().__init__(f"Книга с id={book_id} уже существует")
        self.book_id = book_id


class ReaderAlreadyExistsError(LibraryError):
    def __init__(self, reader_id):
        super().__init__(f"Читатель с id={reader_id} уже существует")
        self.reader_id = reader_id


class BookNotFoundError(LibraryError):
    def __init__(self, book_id):
        super().__init__(f"Книга {book_id} не найдена")
        self.book_id = book_id


class ReaderNotFoundError(LibraryError):
    def __init__(self, reader_id):
        super().__init__(f"Читатель {reader_id} не найден")
        self.reader_id = reader_id


class BookNotAvailableError(LibraryError):
    def __init__(self, book_id):
        super().__init__(f"Книга {book_id} уже выдана")
        self.book_id = book_id