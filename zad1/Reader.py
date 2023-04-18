import json
from copy import deepcopy

from zad1.QuitError import QuitError
# from zad1.System import manage_context
from zad1.User import User
from datetime import date, timedelta


def manage_context(args, rtn=False):
    args_with_quit = deepcopy(args)
    args_with_quit.append("Quit")
    if rtn:
        args_with_quit.insert(len(args_with_quit) - 1, "Return")
    for i, line in enumerate(args_with_quit):
        print(f"{i + 1}. {line}")
    while True:
        try:
            choice = int(input("Choose option: "))
            if choice == len(args_with_quit):
                raise QuitError("User used quit")
            return args_with_quit[choice - 1]
        except IndexError:
            print("Option does not exist! Choose again!")
        except ValueError:
            print("Enter a number!")


class Reader(User):
    READER_DB = 'data/readers_new.json'

    def __init__(self, user_data):
        context = {
            # "Borrow book": self.borrow_book_loop,
            # "Reserve book": self.reserve_book_loop,
            "Prolong book rental": self.prolong_books_rental_loop,
        }

        super().__init__(user_data, context)
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
                data = json.load(rf)
                borrowed_books = data["users"][self.email]["borrowed_books"]
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
                rf.seek(0)
                rf.write(json.dumps(data, indent=4))
                rf.truncate()
                print(f"Date prolonging was successful! New date is {end_date}")
                return True
        except ValueError as err:
            print(f'Number of days must be number!')

# context -> view catalog, my books
# view catalog -> books , search by name, author, tags-> borrow, reserve
# my books -> books -> prolong
