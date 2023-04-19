import json
from utils import manage_context
from zad1.Librarian import Librarian
from zad1.QuitError import QuitError
from zad1.Reader import Reader


class System:
    # def __init__(self):

    # self.STANDARD_CONTEXT = {
    #     Reader: self.STANDARD_READER_CONTEXT,
    #     Librarian: self.STANDARD_LIBRARIAN_CONTEXT
    # }

    def login(self):
        print("Welcome to our library!")
        print("As who do you want to login?:")
        user_type = manage_context(["Reader", "Librarian"])
        match user_type:
            case 'Librarian':
                return Librarian(self.validate_credentials("data/librarians.json"))
            case 'Reader':
                return Reader(self.validate_credentials("data/readers.json"))

    def create_standard_context(self, user):
        context = user.standard_context
        # print(context)
        while True:
            # TODO create more generic function that will take contexts
            choice: str = manage_context(list(context.keys()))
            if choice == "Return":
                break
            context[choice]()

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
