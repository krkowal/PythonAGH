import json

from utils import manage_context


class User:
    READER_DB = 'data/readers_new.json'
    LIBRARIAN_DB = 'data/librarians.json'
    BOOKS_DB = 'data/books.json'

    def __init__(self, user_data, context, catalog_context):
        self.email = user_data["email"]
        self.password = user_data["password"]
        self.standard_context = context
        self.standard_context["View catalog"] = self.view_catalog
        self.catalog_context = catalog_context

    def get_book_list(self):
        with open(self.BOOKS_DB, 'r') as bf:
            books_data = json.load(bf)
            return [f"Title: {book['title']}, id: {book['id']}" for book in books_data["books"]]

    def view_catalog(self, books=None):
        while True:
            if books is None:
                book_list = self.get_book_list()
            else:
                if books == []:
                    print("")
                book_list = books
            book_list.append("Search")
            choice: str = manage_context(book_list, True)
            if choice == "Return":
                break
            if choice == "Search":
                self.search_catalog()
            else:
                book_id = int(choice.split(": ")[-1])
                self.get_book_context(book_id)

    def get_book_context(self, id: int):
        while True:
            choice: str = manage_context(list(self.catalog_context), True)
            if choice == "Return":
                break

            self.catalog_context[choice](id)

    def search_catalog(self):
        phrase = input("Search by phrase: ")
        with open(self.BOOKS_DB, 'r') as bf:
            books_data = json.load(bf)["books"]
            filtered_books = list(filter(lambda book: phrase.upper() in book["title"].upper() or phrase in book[
                "author"].upper() or phrase.lower() in book["tags"], books_data))
            mapped_books = list(map(lambda book: f"Title: {book['title']}, id: {book['id']}", filtered_books))
            self.view_catalog(mapped_books)
