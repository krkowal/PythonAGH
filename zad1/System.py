import json
from copy import deepcopy

from zad1.Book import Book
from zad1.Librarian import Librarian
from zad1.QuitError import QuitError
from zad1.Reader import Reader


class System:
    def __init__(self):
        self.STANDARD_READER_CONTEXT = {
            "Borrow book": self.borrow_book_loop,
            "Reserve book": self.reserve_book_loop,
            "Prolong book rental": self.prolong_book_rental,
            "View catalog": self.view_catalog,
        }
        self.STANDARD_LIBRARIAN_CONTEXT = {
            "placeholder": "placeholder"
        }
        self.STANDARD_CONTEXT = {
            Reader: self.STANDARD_READER_CONTEXT,
            Librarian: self.STANDARD_LIBRARIAN_CONTEXT
        }

    def login(self):
        print("Welcome to our library!")
        print("As who do you want to login?:")
        user_type = self.show_context(["Reader", "Librarian"])
        match user_type:
            case 'Librarian':
                return Librarian(self.validate_credentials("data/librarians.json"))
            case 'Reader':
                return Reader(self.validate_credentials("data/readers.json"))

    # def reader_context(self, user):
    #
    #     while True:
    #         choice: str = self.show_context(list(self.STANDARD_READER_CONTEXT.keys()))
    #
    #         self.STANDARD_READER_CONTEXT[choice]()
    #
    # def librarian_context(self, user):
    #     print("librarian context")

    def view_context(self, user):
        context: dict[str,] = self.STANDARD_CONTEXT[user.__class__]
        # TODO maybe move contexts to User and librarian functions
        print(context)
        while True:
            # TODO remove True and create more generic function that will take contexts
            choice: str = self.show_context(list(context.keys()), True)
            if choice == "Return":
                break
            context[choice]()

    def show_context(self, args, rtn=False):
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

    def validate_credentials(self, db_path):
        while True:
            print("Enter credentials!")
            email = input("email: ")
            password = input("password: ")
            with open(db_path, 'r') as file:
                data = json.load(file)
                users = data["users"]
                # print(users)
                for user in users:
                    if user["email"] == email and user["password"] == password:
                        return user
            print("Email or password incorrect!")

    def borrow_book_loop(self):
        print("Borrow book loop")

    def reserve_book_loop(self):
        print("reserve_book_loop")

    def prolong_book_rental(self):
        print("prolong book rental loop")

    def view_catalog(self):
        print("view catalog loop")
