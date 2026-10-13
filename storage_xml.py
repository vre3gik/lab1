import xml.etree.ElementTree as ET

from models import Book, EBook, Library, Reader


class XmlStorage:
    @staticmethod
    def save(lib: Library, path: str) -> None:
        root = ET.Element("library", name=lib.name)

        books_el = ET.SubElement(root, "books")
        for b in lib.books:
            attrs = {
                "type": "EBook" if isinstance(b, EBook) else "Book",
                "id": str(b.id),
                "title": b.title,
                "author": b.author,
                "available": str(b.available).lower(),
            }
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

    @staticmethod
    def load(path: str) -> Library:
        root = ET.parse(path).getroot()
        lib = Library(root.attrib["name"])

        for b_el in root.find("books"):
            a = b_el.attrib
            if a["type"] == "EBook":
                lib.books.append(EBook(
                    int(a["id"]), a["title"], a["author"],
                    float(a["size_mb"]), a["format"],
                    a["available"] == "true",
                ))
            else:
                lib.books.append(Book(
                    int(a["id"]), a["title"], a["author"],
                    a["available"] == "true",
                ))

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
