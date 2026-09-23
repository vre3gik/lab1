import json
import xml.etree.ElementTree as ET


class LibraryError(Exception):
    pass


class Book:
    def __init__(self, id, title, author, available=True):
        self.id = id
        self.title = title
        self.author = author
        self.available = available

    def to_dict(self):
        return {"type": "Book", "id": self.id, "title": self.title,
                "author": self.author, "available": self.available}

    def __str__(self):
        return f"[{self.id}] «{self.title}» — {self.author} " \
               f"({'свободна' if self.available else 'выдана'})"


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
            raise LibraryError(f"Книга {book.id} уже выдана")
        book.available = False
        self.taken.append(book)

    def give_back(self, book):
        if book in self.taken:
            self.taken.remove(book)
            book.available = True

    def to_dict(self):
        return {"id": self.id, "name": self.name,
                "taken_ids": [b.id for b in self.taken]}

    def __str__(self):
        return f"[{self.id}] {self.name} (взято: {len(self.taken)})"


class Library:
    def __init__(self, name="Библиотека"):
        self.name = name
        self.books = []
        self.readers = []

    def add_book(self, book):
        if any(b.id == book.id for b in self.books):
            raise LibraryError(f"Книга с id={book.id} уже существует")
        self.books.append(book)

    def add_reader(self, reader):
        if any(r.id == reader.id for r in self.readers):
            raise LibraryError(f"Читатель с id={reader.id} уже существует")
        self.readers.append(reader)

    def find_book(self, id):
        for b in self.books:
            if b.id == id:
                return b
        raise LibraryError(f"Книга {id} не найдена")

    def find_reader(self, id):
        for r in self.readers:
            if r.id == id:
                return r
        raise LibraryError(f"Читатель {id} не найден")

    def lend(self, book_id, reader_id):
        self.find_reader(reader_id).borrow(self.find_book(book_id))

    def give_back(self, book_id, reader_id):
        self.find_reader(reader_id).give_back(self.find_book(book_id))


def save_json(lib, path):
    data = {
        "name": lib.name,
        "books": [b.to_dict() for b in lib.books],
        "readers": [r.to_dict() for r in lib.readers],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    lib = Library(data["name"])
    for bd in data["books"]:
        if bd["type"] == "EBook":
            lib.books.append(EBook(bd["id"], bd["title"], bd["author"],
                                   bd["size_mb"], bd["format"], bd["available"]))
        else:
            lib.books.append(Book(bd["id"], bd["title"], bd["author"], bd["available"]))
    for rd in data["readers"]:
        r = Reader(rd["id"], rd["name"])
        for bid in rd["taken_ids"]:
            for b in lib.books:
                if b.id == bid:
                    r.taken.append(b)
                    b.available = False
        lib.readers.append(r)
    return lib


def save_xml(lib, path):
    root = ET.Element("library", name=lib.name)
    books_el = ET.SubElement(root, "books")
    for b in lib.books:
        attrs = {"type": "EBook" if isinstance(b, EBook) else "Book",
                 "id": str(b.id), "title": b.title, "author": b.author,
                 "available": str(b.available).lower()}
        if isinstance(b, EBook):
            attrs["size_mb"] = str(b.size_mb)
            attrs["format"] = b.format
        ET.SubElement(books_el, "book", **attrs)

    readers_el = ET.SubElement(root, "readers")
    for r in lib.readers:
        r_el = ET.SubElement(readers_el, "reader", id=str(r.id), name=r.name)
        for b in r.taken:
            ET.SubElement(r_el, "taken", book_id=str(b.id))

    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def load_xml(path):
    root = ET.parse(path).getroot()
    lib = Library(root.attrib["name"])

    for b_el in root.find("books"):
        a = b_el.attrib
        if a["type"] == "EBook":
            lib.books.append(EBook(int(a["id"]), a["title"], a["author"],
                                   float(a["size_mb"]), a["format"],
                                   a["available"] == "true"))
        else:
            lib.books.append(Book(int(a["id"]), a["title"], a["author"],
                                  a["available"] == "true"))
    for r_el in root.find("readers"):
        r = Reader(int(r_el.attrib["id"]), r_el.attrib["name"])
        for t in r_el.findall("taken"):
            bid = int(t.attrib["book_id"])
            for b in lib.books:
                if b.id == bid:
                    r.taken.append(b)
                    b.available = False
        lib.readers.append(r)
    return lib


MENU = """
=== Библиотека ===
  1. Показать книги
  2. Показать читателей
  3. Добавить книгу
  4. Добавить читателя
  5. Выдать книгу
  6. Вернуть книгу
  7. Сохранить в JSON
  8. Загрузить из JSON
  9. Сохранить в XML
 10. Загрузить из XML
  0. Выход
"""


def main():
    lib = Library("Городская библиотека")
    lib.add_book(Book(1, "Война и мир", "Толстой"))
    lib.add_book(Book(2, "Преступление и наказание", "Достоевский"))
    lib.add_book(EBook(3, "Python", "Рамальо", 12.5, "PDF"))
    lib.add_reader(Reader(101, "Иван"))
    lib.add_reader(Reader(102, "Пётр"))
    while True:
        print(MENU)
        choice = input("Выбор: ").strip()
        try:
            if choice == "1":
                for b in lib.books:
                    print(" ", b)
            elif choice == "2":
                for r in lib.readers:
                    print(" ", r)
            elif choice == "3":
                id = int(input("  id: "))
                title = input("  название: ")
                author = input("  автор: ")
                lib.add_book(Book(id, title, author))
                print("  + добавлено")
            elif choice == "4":
                id = int(input("  id: "))
                name = input("  имя: ")
                lib.add_reader(Reader(id, name))
                print("  + добавлено")
            elif choice == "5":
                lib.lend(int(input("  book_id: ")), int(input("  reader_id: ")))
                print("  + выдано")
            elif choice == "6":
                lib.give_back(int(input("  book_id: ")), int(input("  reader_id: ")))
                print("  + возвращено")
            elif choice == "7":
                save_json(lib, input("  путь: "))
                print("  + сохранено")
            elif choice == "8":
                lib = load_json(input("  путь: "))
                print("  + загружено")
            elif choice == "9":
                save_xml(lib, input("  путь: "))
                print("  + сохранено")
            elif choice == "10":
                lib = load_xml(input("  путь: "))
                print("  + загружено")
            elif choice == "0":
                print("Поставьте 5!")
                break
            else:
                print("  ? неизвестная команда")
        except LibraryError as e:
            print(f"  ! Ошибка: {e}")
        except ValueError as e:
            print(f"  ! Плохие данные: {e}")
        except FileNotFoundError:
            print("  ! Файл не найден")
        except Exception as e:
            print(f"  ! Ошибка: {e}")


if __name__ == "__main__":
    main()
