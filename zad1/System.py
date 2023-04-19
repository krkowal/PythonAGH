import json
from utils import manage_context
from zad1.Librarian import Librarian
from zad1.QuitError import QuitError
from zad1.Reader import Reader


class System:
    READER_DB = 'data/readers_new.json'
    LIBRARIAN_DB = 'data/librarians.json'

    def login(self):
        print("Welcome to our library!")
        print("As who do you want to login?:")
        user_type = manage_context(["Reader", "Librarian"])
        match user_type:
            case 'Librarian':
                return Librarian(self.validate_credentials(self.LIBRARIAN_DB))
            case 'Reader':
                return Reader(self.validate_credentials(self.READER_DB))

    def create_standard_context(self, user):
        context = user.standard_context
        while True:
            choice: str = manage_context(list(context.keys()))
            if choice == "Return":
                break
            context[choice]()

    def validate_credentials(self, db_path):
        try:
            print("Enter credentials!")
            email = input("email: ")
            password = input("password: ")
            with open(db_path, 'r') as file:
                data = json.load(file)
                users = data["users"]

                if users[email]["password"] == password:
                    return {"email": email} | users[email]
        except ValueError:
            print("Email or password incorrect!")
