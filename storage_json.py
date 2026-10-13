import json

from models import Book, EBook, Library, Reader


class JsonStorage:
    @staticmethod
    def save(lib: Library, path: str) -> None:
        data = {
            "name": lib.name,
            "books": [b.to_dict() for b in lib.books],
            "readers": [r.to_dict() for r in lib.readers],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load(path: str) -> Library:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        lib = Library(data["name"])

        for bd in data["books"]:
            if bd["type"] == "EBook":
                lib.books.append(EBook(
                    bd["id"], bd["title"], bd["author"],
                    bd["size_mb"], bd["format"], bd["available"],
                ))
            else:
                lib.books.append(Book(
                    bd["id"], bd["title"], bd["author"], bd["available"],
                ))

        for rd in data["readers"]:
            r = Reader(rd["id"], rd["name"])
            for bid in rd["taken_ids"]:
                for b in lib.books:
                    if b.id == bid:
                        r.taken.append(b)
                        b.available = False
            lib.readers.append(r)

        return lib
