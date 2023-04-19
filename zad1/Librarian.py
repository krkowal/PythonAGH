import json

from zad1.User import User
from utils import manage_context


class Librarian(User):
    def __init__(self, user_data):
        standard_context = {
            "Take in return": self.take_in_return,
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

    def take_in_return(self):
        print("take in book return loop")

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
        print("remove book loop")

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

    def show_book_data(self):
        print("show book data loop")
# context -> take in return, add new book, remove book, add reader, view catalog
# take in return -> user_email and book_id
# add new book -> book data
# remove book -> book_id
# add reader -> reader data
# view catalog -> books -> see if book is borrowed and who borrowed it and when it is available
