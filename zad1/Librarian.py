import json

from zad1.User import User
from utils import manage_context


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
            with open(self.BOOKS_DB, 'r+') as bf:
                with open(self.READER_DB, 'r+') as rf:
                    books_data = json.load(bf)
                    reader_data = json.load(rf)
                    book = {}
                    for b in books_data["books"]:
                        if b["id"] == book_id:
                            book = b
                    if book is {}:
                        print("Book no longer exists!")
                        return False
                    user, user_book = "", {}
                    for u in reader_data["users"]:
                        for b in reader_data["users"][u]["borrowed_books"]:
                            if b["id"] == book_id:
                                print("inside")
                                user, user_book = u, b
                    if user == "" or user_book is {}:
                        print("This book is not borrowed")
                        return False
                    book.update({
                        "borrowed_by": "",
                        "borrowed_until": ""
                    })
                    print(user_book)
                    reader_data["users"][user]["borrowed_books"].remove(user_book)
                    bf.seek(0)
                    bf.write(json.dumps(books_data, indent=4))
                    bf.truncate()
                    rf.seek(0)
                    rf.write(json.dumps(reader_data, indent=4))
                    rf.truncate()
                    print("Book was successfully returned")
                    return True
        except ValueError:
            print("Id should be a number!")

    def add_new_book(self):
        book = {}
        book['title'] = input("Enter title: ")
        book['author'] = input("Enter author: ")
        book['tags'] = input("Enter tags (comma separated): ").strip().split(",")
        with open(self.BOOKS_DB, 'r+') as bf:
            books_data = json.load(bf)
            book = {"id": max(books_data["books"], key=lambda b: b["id"])["id"] + 1} | book
            book |= {
                "borrowed_by": "",
                "borrowed_until": "",
                "reserved_by": "",
                "reserved_until": ""
            }
            print(book)
            books_data["books"].append(book)
            bf.seek(0)
            bf.write(json.dumps(books_data, indent=4))
            bf.truncate()
            print("Book was added successfully")

    def remove_book(self):
        try:
            book_id = int(input("Enter book's id: "))
            with open(self.BOOKS_DB, 'r+') as bf:
                with open(self.READER_DB, 'r') as rf:
                    books_data = json.load(bf)
                    reader_data = json.load(rf)
                    book = {}
                    for b in books_data["books"]:
                        if b["id"] == book_id:
                            book = b
                    if book is {}:
                        print("Book does not exist!")
                        return False
                    for u in reader_data["users"]:
                        for b in reader_data["users"][u]["borrowed_books"]:
                            if b["id"] == book_id:
                                print("Book is borrowed, therefore cannot be removed!")
                                return False
                    books_data["books"].remove(book)
                    bf.seek(0)
                    bf.write(json.dumps(books_data, indent=4))
                    bf.truncate()
                    print("Book was successfully removed")
                    return True
        except ValueError:
            print("Id should be a number!")

    def add_reader(self):
        while True:
            email = input("Enter email: ")
            password = input("Enter password: ")
            with open(self.READER_DB, 'r+') as rf:
                reader_data = json.load(rf)
                if email in reader_data["users"]:
                    print("Users already exists!")
                    continue
                new_user = {
                    "password": password,
                    "borrowed_books": [],
                    "reserved_books": []
                }
                reader_data["users"][email] = new_user
                rf.seek(0)
                rf.write(json.dumps(reader_data, indent=4))
                rf.truncate()
                print("User was successfully created!")
                break

    def show_book_data(self, book_id: int):
        with open(self.BOOKS_DB, 'r') as bf:
            books_data = json.load(bf)
            book = {}
            for b in books_data["books"]:
                if b["id"] == book_id:
                    book = b
            for field in book:
                print(f"Book {field}: {book[field]}")
            manage_context([], True)
