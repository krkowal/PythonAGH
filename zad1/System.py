import json
from copy import deepcopy

from zad1.Book import Book
from zad1.Librarian import Librarian
from zad1.QuitError import QuitError
from zad1.Reader import Reader


class System:

    def login(self):
        print("Welcome to our library!")
        print("As who do you want to login?:")
        user_type = self.show_context(["Reader", "Librarian"])
        match user_type:
            case 'Librarian':
                return Librarian(self.validate_credentials("data/librarians.json"))
            case 'Reader':
                return Reader(self.validate_credentials("data/readers.json"))

    def show_context(self, args):
        args_with_quit = deepcopy(args)
        args_with_quit.append("Quit")
        for i, line in enumerate(args_with_quit):
            print(f"{i + 1}. {line}")
        while True:
            try:
                choice = int(input("Choose option: "))
                if choice == len(args) + 1:
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
