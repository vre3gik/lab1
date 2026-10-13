from menu import ConsoleMenu
from models import Book, EBook, Library, Reader


def create_demo_library() -> Library:
    lib = Library("Городская библиотека")
    lib.add_book(Book(1, "Война и мир", "Толстой"))
    lib.add_book(Book(2, "Преступление и наказание", "Достоевский"))
    lib.add_book(EBook(3, "Python", "Рамальо", 12.5, "PDF"))
    lib.add_reader(Reader(101, "Иван"))
    lib.add_reader(Reader(102, "Пётр"))
    return lib


def main():
    library = create_demo_library()
    menu = ConsoleMenu(library)
    menu.run()


if __name__ == "__main__":
    main()
