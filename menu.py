from exceptions import LibraryError
from models import Book, EBook, Library, Reader
from storage_json import JsonStorage
from storage_xml import XmlStorage

MENU_TEXT = """
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


class ConsoleMenu:
    def __init__(self, library: Library):
        self.library = library

    def _show_books(self):
        print("  Список книг:")
        if not self.library.books:
            print("  (пусто)")
            return
        for b in self.library.books:
            print(" ", b)

    def _show_readers(self):
        print("  Список читателей:")
        if not self.library.readers:
            print("  (пусто)")
            return
        for r in self.library.readers:
            print(" ", r)

    def _add_book(self):
        print("  Добавление книги")
        book_id = int(input("  id: "))
        title = input("  название: ")
        author = input("  автор: ")
        self.library.add_book(Book(book_id, title, author))
        print("  + добавлено")

    def _add_reader(self):
        print("  Добавление читателя")
        reader_id = int(input("  id: "))
        name = input("  имя: ")
        self.library.add_reader(Reader(reader_id, name))
        print("  + добавлено")

    def _lend(self):
        print("  Выдача книги")
        book_id = int(input("  book_id: "))
        reader_id = int(input("  reader_id: "))
        self.library.lend(book_id, reader_id)
        print("  + выдано")

    def _give_back(self):
        print("  Возврат книги")
        book_id = int(input("  book_id: "))
        reader_id = int(input("  reader_id: "))
        self.library.give_back(book_id, reader_id)
        print("  + возвращено")

    def _save_json(self):
        print("  Сохранение в JSON")
        path = input("  путь: ")
        JsonStorage.save(self.library, path)
        print("  + сохранено")

    def _load_json(self):
        print("  Загрузка из JSON")
        path = input("  путь: ")
        self.library = JsonStorage.load(path)
        print("  + загружено")

    def _save_xml(self):
        print("  Сохранение в XML")
        path = input("  путь: ")
        XmlStorage.save(self.library, path)
        print("  + сохранено")

    def _load_xml(self):
        print("  Загрузка из XML")
        path = input("  путь: ")
        self.library = XmlStorage.load(path)
        print("  + загружено")

    def _get_actions(self):
        return {
            "1": self._show_books,
            "2": self._show_readers,
            "3": self._add_book,
            "4": self._add_reader,
            "5": self._lend,
            "6": self._give_back,
            "7": self._save_json,
            "8": self._load_json,
            "9": self._save_xml,
            "10": self._load_xml,
        }

    def run(self):
        actions = self._get_actions()
        while True:
            print(MENU_TEXT)
            choice = input("Выбор: ").strip()

            if choice == "0":
                print("Поставьте 5!")
                break

            try:
                action = actions.get(choice)
                if action is None:
                    print("  ? неизвестная команда")
                else:
                    action()
            except LibraryError as e:
                print(f"  ! Ошибка: {e}")
            except ValueError as e:
                print(f"  ! Плохие данные: {e}")
            except FileNotFoundError:
                print("  ! Файл не найден")
            except Exception as e:
                print(f"  ! Ошибка: {e}")
