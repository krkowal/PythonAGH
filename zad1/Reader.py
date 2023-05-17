from datetime import date, timedelta

from User import User
from utils import manage_context, get_data, save_data, get_book_by_id


class Reader(User):

    def __init__(self, user_data):
        context: dict[str,] = {
            "Prolong book rental": self.prolong_books_rental_loop,
        }
        catalog_context: dict[str,] = {
            "Borrow this book": self.borrow_book,
            "Reserve this book": self.reserve_book,
        }
        super().__init__(user_data, context, catalog_context)
        self.borrowed_books = user_data["borrowed_books"]
        self.BOOK_CONTEXT: dict[str,] = {
            "Prolong": self.prolong_book
        }

    def __str__(self):
        return f"Reader\nEmail: {self.email}\nPassword: {self.password}\nBorrowed books: {self.borrowed_books}"

    def get_borrowed_books(self):
        return get_data(self.READER_DB)["users"][self.email]["borrowed_books"]

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
            days = int(input("How many days (max 14) do you want to prolong the book?: "))
            while days > 14 or days < 0:
                print('Number of days should be between 0 and 14')
                days = int(input("How many days (max 14) do you want to prolong the book?: "))
            user_data = get_data(self.READER_DB)
            book_data = get_data(self.BOOKS_DB)
            borrowed_books = user_data["users"][self.email]["borrowed_books"]
            book = get_book_by_id(book_id, borrowed_books)
            if book is {}:
                print("Book no longer exists in profile!")

            return_date = book["borrowed_until"]
            print(f"Current return date: {return_date}")
            reserved = book["reserved_until"]
            if reserved != "":
                print("The book has been already reserved! You cannot prolong the book!")
                return False

            end_date = date.fromisoformat(return_date)
            end_date += timedelta(days=days)
            book["borrowed_until"] = end_date.__str__()

            db_book = get_book_by_id(book_id, book_data["books"])
            if db_book == {}:
                raise KeyError
            db_book["borrowed_until"] = end_date.__str__()
            save_data(self.BOOKS_DB, book_data)
            save_data(self.READER_DB, user_data)
            print(f"Date prolonging was successful! New date is {end_date}")
        except ValueError:
            print(f'Number of days must be number!')
        except KeyError:
            print("Book no longer appears in database!")

    def borrow_book(self, book_id):
        try:
            books_data = get_data(self.BOOKS_DB)
            reader_data = get_data(self.READER_DB)
            book = get_book_by_id(book_id, books_data["books"])
            if book is {}:
                raise KeyError
            if book["borrowed_by"] != "":
                print("Book is already borrowed!")
                return False
            if book["reserved_by"] != "":
                if book["reserved_by"] == self.email:
                    book["reserved_by"] = ""
                    book["reserved_until"] = ""
                    reserved_books = reader_data["users"][self.email]["reserved_books"]
                    user_reserved_book = get_book_by_id(book_id, reserved_books)
                    reserved_books.remove(user_reserved_book)
                else:
                    print("Book is already reserved!")
                    return False
            book["borrowed_by"] = self.email
            book["borrowed_until"] = (date.today() + timedelta(days=28)).__str__()
            reader_data["users"][self.email]["borrowed_books"].append(book)
            save_data(self.BOOKS_DB, books_data)
            save_data(self.READER_DB, reader_data)
            print(f"Book was borrowed successfully! Current end date of rental: {book['borrowed_until']}")
            return True
        except KeyError:
            print("Book no longer exists!")

    def reserve_book(self, book_id):
        try:
            books_data = get_data(self.BOOKS_DB)
            reader_data = get_data(self.READER_DB)
            book = get_book_by_id(book_id, books_data["books"])
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
                borrowed_book = get_book_by_id(book_id, user_borrowed_books)
                borrowed_book["reserved_by"] = self.email
                borrow_end = date.fromisoformat(book["borrowed_until"])
                reserve_end_date = (borrow_end + timedelta(days=28)).__str__()
                book["reserved_until"] = reserve_end_date
                borrowed_book["reserved_until"] = reserve_end_date
            else:
                book["reserved_until"] = (date.today() + timedelta(days=28)).__str__()
            reader_data["users"][self.email]["reserved_books"].append(book)
            save_data(self.BOOKS_DB, books_data)
            save_data(self.READER_DB, reader_data)
            print(f"Book was reserved successfully! Current end date of reservation: {book['reserved_until']}")
            return True
        except KeyError:
            print("Book no longer exists!")
