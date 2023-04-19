import json
from utils import manage_context
from zad1.User import User
from datetime import date, timedelta


class Reader(User):

    def __init__(self, user_data):
        context = {
            # "Borrow book": self.borrow_book_loop,
            # "Reserve book": self.reserve_book_loop,
            "Prolong book rental": self.prolong_books_rental_loop,
        }
        catalog_context = {
            "Borrow this book": self.borrow_book,
            "Reserve this book": self.reserve_book,

        }

        super().__init__(user_data, context, catalog_context)
        self.borrowed_books = user_data["borrowed_books"]
        self.BOOK_CONTEXT = {
            "Prolong": self.prolong_book
        }

    def __str__(self):
        return f"Reader\nEmail: {self.email}\nPassword: {self.password}\nBorrowed books: {self.borrowed_books}"

    # def borrow_book_loop(self):
    #     print("Borrow book loop")
    #
    # def reserve_book_loop(self):
    #     print("reserve_book_loop")

    def get_borrowed_books(self):
        with open(self.READER_DB, 'r') as read_file:
            data = json.load(read_file)["users"]
            return data[self.email]["borrowed_books"]

    def get_borrowed_books_titles(self):
        return [book["title"] for book in self.get_borrowed_books()]

    def get_prolong_context(self):
        return {f"Title: {book['title']}, id: {book['id']}": self.prolong_book_loop for book in
                self.get_borrowed_books()}

    def prolong_books_rental_loop(self):
        while True:
            choice: str = manage_context(list(self.get_prolong_context()), True)
            if choice == "Return":
                break
            self.get_prolong_context()[choice](choice)

    def prolong_book_loop(self, title_string: str):
        book_id = int(title_string.split(": ")[-1])
        while True:
            choice: str = manage_context(list(self.BOOK_CONTEXT.keys()), True)
            if choice == "Return":
                break
            self.BOOK_CONTEXT[choice](book_id)

    def prolong_book(self, book_id: int):
        try:
            with open(self.READER_DB, 'r+') as rf:
                with open(self.BOOKS_DB, 'r+') as bf:
                    user_data = json.load(rf)
                    book_data = json.load(bf)
                    borrowed_books = user_data["users"][self.email]["borrowed_books"]
                    book = {}
                    for b in borrowed_books:
                        if book_id == b['id']:
                            book = b
                    if book is {}:
                        print("Book no longer exists in profile!")

                    return_date = book["borrowed_until"]
                    print(f"Current return date: {return_date}")
                    reserved = book["reserved_until"]
                    if reserved != "":
                        print("The book has been already reserved! You cannot prolong the book!")
                        return False

                    days = int(input("How many days (max 14) do you want to prolong the book?: "))
                    while days > 14 or days < 0:
                        print('Number of days should be between 0 and 14')
                        days = int(input("How many days (max 14) do you want to prolong the book?: "))
                    end_date = date.fromisoformat(return_date)
                    end_date += timedelta(days=days)
                    book["borrowed_until"] = end_date.__str__()

                    db_book = {}
                    for book in book_data["books"]:
                        if book["id"] == book_id:
                            db_book = book
                    if db_book == {}:
                        raise KeyError
                    db_book["borrowed_until"] = end_date.__str__()
                    bf.seek(0)
                    bf.write(json.dumps(book_data, indent=4))
                    bf.truncate()
                    rf.seek(0)
                    rf.write(json.dumps(user_data, indent=4))
                    rf.truncate()

                    print(f"Date prolonging was successful! New date is {end_date}")

        except ValueError as err:
            print(f'Number of days must be number!')
        except KeyError as err:
            print("Book no longer appears in database!")

    def borrow_book(self, id):
        try:
            with open(self.BOOKS_DB, 'r+') as bf:
                with open(self.READER_DB, 'r+') as rf:
                    books_data = json.load(bf)
                    reader_data = json.load(rf)
                    book = {}
                    for b in books_data["books"]:
                        if b["id"] == id:
                            book = b
                    if book is {}:
                        raise KeyError
                    if book["borrowed_by"] != "" or book["reserved_by"] != "":
                        print("Book is already borrowed or reserved!")
                        return False
                    book["borrowed_by"] = self.email
                    book["borrowed_until"] = (date.today() + timedelta(days=28)).__str__()
                    reader_data["users"][self.email]["borrowed_books"].append(book)
                    bf.seek(0)
                    bf.write(json.dumps(books_data, indent=4))
                    bf.truncate()
                    rf.seek(0)
                    rf.write(json.dumps(reader_data, indent=4))
                    rf.truncate()
                    print(f"Book was borrowed successfully! Current end date of rental: {book['borrowed_until']}")
                    return True

        except KeyError:
            print("Book no longer exists!")

    def reserve_book(self, book_id):
        try:
            with open(self.BOOKS_DB, 'r+') as bf:
                with open(self.READER_DB, 'r+') as rf:
                    books_data = json.load(bf)
                    reader_data = json.load(rf)
                    book = {}

                    for b in books_data["books"]:
                        if b["id"] == book_id:
                            book = b
                    if book is {}:
                        raise KeyError
                    if book["reserved_by"] != "":
                        print("Book is already reserved!")
                        return False
                    book_borrowed_by = book["borrowed_by"]
                    if book_borrowed_by == self.email:
                        print("Book has been already borrowed by You!")
                        return False
                    book["reserved_by"] = self.email

                    if book_borrowed_by != "":
                        user_borrowed_books = reader_data["users"][book_borrowed_by]["borrowed_books"]
                        borrowed_book = {}
                        for b in user_borrowed_books:
                            if b['id'] == book_id:
                                borrowed_book = b
                        borrowed_book["reserved_by"] = self.email
                        borrow_end = date.fromisoformat(book["borrowed_until"])
                        reserve_end_date = (borrow_end + timedelta(days=28)).__str__()
                        book["reserved_until"] = reserve_end_date
                        borrowed_book["reserved_until"] = reserve_end_date
                    reader_data["users"][self.email]["reserved_books"].append(book)
                    bf.seek(0)
                    bf.write(json.dumps(books_data, indent=4))
                    bf.truncate()
                    rf.seek(0)
                    rf.write(json.dumps(reader_data, indent=4))
                    rf.truncate()
                    print(f"Book was reserved successfully! Current end date of reservation: {book['reserved_until']}")
                    return True

        except KeyError as err:
            print(err)
            print("Book no longer exists!")
# context -> view catalog, my books
# view catalog -> books , search by name, author, tags-> borrow, reserve
# my books -> books -> prolong
