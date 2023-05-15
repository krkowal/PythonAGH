from Constants import READER_DB, LIBRARIAN_DB, BOOKS_DB
from utils import manage_context, get_data


class User:
    READER_DB = READER_DB
    LIBRARIAN_DB = LIBRARIAN_DB
    BOOKS_DB = BOOKS_DB

    def __init__(self, user_data, context, catalog_context):
        self.email = user_data["email"]
        self.password = user_data["password"]
        self.standard_context = context
        self.standard_context["View catalog"] = self.view_catalog
        self.catalog_context = catalog_context

    def get_book_list(self):
        books_data = get_data(self.BOOKS_DB)
        return [f"Title: {book['title']}, id: {book['id']}" for book in books_data["books"]]

    def view_catalog(self, books=None):
        while True:
            if books is None:
                book_list = self.get_book_list()
                book_list.append("Search")
            else:
                book_list = books
            choice: str = manage_context(book_list, True)
            if choice == "Return":
                break
            if choice == "Search":
                self.search_catalog()
            else:
                book_id = int(choice.split(": ")[-1])
                self.get_book_context(book_id)

    def get_book_context(self, book_id: int):
        while True:
            choice: str = manage_context(list(self.catalog_context), True)
            if choice == "Return":
                break

            self.catalog_context[choice](book_id)

    def search_catalog(self):
        phrase = input("Search by phrase: ")
        books_data = get_data(self.BOOKS_DB)["books"]
        filtered_books = list(filter(lambda book: phrase.upper() in book["title"].upper() or phrase in book[
            "author"].upper() or phrase.lower() in book["tags"], books_data))  # polecam list comprehension
        mapped_books = list(map(lambda book: f"Title: {book['title']}, id: {book['id']}", filtered_books))
        if not mapped_books:
            print("No matches")
        self.view_catalog(mapped_books)
