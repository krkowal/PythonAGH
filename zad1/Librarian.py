from User import User
from utils import manage_context, get_book_by_id, get_data, save_data


class Librarian(User):
    def __init__(self, user_data):
        standard_context = {
            "Return book": self.return_book,
            "Add new book": self.add_new_book,
            "Remove book": self.remove_book,
            "Add new reader": self.add_reader,
        }
        catalog_context = {
            "Show data": self.show_book_data
        }
        super().__init__(user_data, standard_context, catalog_context)

    def __str__(self):
        return f"Librarian\nEmail: {self.email}\nPassword: {self.password}"

    def return_book(self):
        try:
            book_id = int(input("Enter book's id: "))
            books_data = get_data(self.BOOKS_DB)
            reader_data = get_data(self.READER_DB)
            book = get_book_by_id(book_id, books_data["books"])
            if book is {}:
                print("Book no longer exists!")
                return False
            user, user_book = "", {}
            for u in reader_data["users"]:
                for b in reader_data["users"][u]["borrowed_books"]:
                    if b["id"] == book_id:
                        user, user_book = u, b
            if user == "" or user_book is {}:
                print("This book is not borrowed")
                return False
            if book["reserved_by"] != "":
                reserved_books = reader_data["users"][books_data["reserved_by"]]["reserved_by"]
                reserved_book = get_book_by_id(book_id, reserved_books)
                reserved_book.update({
                    "borrowed_by": "",
                    "borrowed_until": ""
                })
            book.update({
                "borrowed_by": "",
                "borrowed_until": ""
            })
            reader_data["users"][user]["borrowed_books"].remove(user_book)
            save_data(self.BOOKS_DB, books_data)
            save_data(self.READER_DB, reader_data)
            print("Book was successfully returned")
            return True
        except ValueError:
            print("Id should be a number!")

    def add_new_book(self):
        book = {}
        book['title'] = input("Enter title: ")
        book['author'] = input("Enter author: ")
        book['tags'] = input("Enter tags (comma separated): ").strip().split(",")
        books_data = get_data(self.BOOKS_DB)
        book = {"id": max(books_data["books"], key=lambda b: b["id"])["id"] + 1} | book
        book |= {
            "borrowed_by": "",
            "borrowed_until": "",
            "reserved_by": "",
            "reserved_until": ""
        }
        print(book)
        books_data["books"].append(book)
        save_data(self.BOOKS_DB, books_data)
        print("Book was added successfully")

    def remove_book(self):
        try:
            book_id = int(input("Enter book's id: "))
            books_data = get_data(self.BOOKS_DB)
            reader_data = get_data(self.READER_DB)
            book = get_book_by_id(book_id, books_data["books"])
            if book is {}:
                print("Book does not exist!")
                return False
            for u in reader_data["users"]:
                for b in reader_data["users"][u]["borrowed_books"]:
                    if b["id"] == book_id:
                        print("Book is borrowed, therefore cannot be removed!")
                        return False
            books_data["books"].remove(book)
            save_data(self.BOOKS_DB, books_data)
            print("Book was successfully removed")
            return True
        except ValueError:
            print("Id should be a number!")

    def add_reader(self):
        while True:
            email = input("Enter email: ")
            password = input("Enter password: ")
            reader_data = get_data(self.READER_DB)
            if email in reader_data["users"]:
                print("Users already exists!")
                continue
            new_user = {
                "password": password,
                "borrowed_books": [],
                "reserved_books": []
            }
            reader_data["users"][email] = new_user
            save_data(self.READER_DB, reader_data)
            print("User was successfully created!")
            break

    def show_book_data(self, book_id: int):
        books_data = get_data(self.BOOKS_DB)
        book = get_book_by_id(book_id, books_data["books"])
        for field in book:
            print(f"Book {field}: {book[field]}")
        manage_context([], True)
